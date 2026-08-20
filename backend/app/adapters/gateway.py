"""Primary → validate → memory/db cache → demo fallback.

Database is completely optional and non-blocking. Live market data and analytics
will continue to function even if SQLite or any database engine is unavailable.
"""

from __future__ import annotations

from collections.abc import Callable
import time
from typing import Any, TypeVar

from sqlalchemy.orm import Session

from app.adapters.exceptions import ProviderError
from app.adapters.normalized import FetchResult
from app.adapters.validation import validate_records
from app.core.logging_config import get_logger
from app.database.database import SessionLocal
from app.database.repositories import PersistenceRepository

logger = get_logger("gateway")

T = TypeVar("T")


class DataGateway:
    def __init__(
        self,
        session_factory: Callable[[], Session] = SessionLocal,
    ) -> None:
        self._session_factory = session_factory
        # Instance in-memory TTL cache: key -> (cached_at_timestamp, items, provider_name, data_status, source_state)
        self._cache: dict[str, tuple[float, list[Any], str, str, str]] = {}

    def fetch(
        self,
        *,
        provider_name: str,
        retrieve: Callable[[], list[T]],
        persist: Callable[[PersistenceRepository, list[T]], None] | None = None,
        load_cache: Callable[[PersistenceRepository], list[T]] | None = None,
        fallback: Callable[[], list[T]],
        cache_key: str | None = None,
        ttl_seconds: float = 60.0,
    ) -> FetchResult:
        func_name = getattr(retrieve, "__qualname__", getattr(retrieve, "__name__", str(retrieve))).split(".")[-1]
        key = cache_key or func_name
        now = time.time()

        # 1. Check fresh in-memory cache if primary provider was used
        if key in self._cache and provider_name != "failing":
            cached_at, cached_items, cached_provider, cached_status, cached_source = self._cache[key]
            if now - cached_at < ttl_seconds and cached_items:
                return FetchResult(
                    items=cached_items,
                    source_state=cached_source,
                    data_status=cached_status,
                    provider=cached_provider,
                )

        # 2. Attempt live provider retrieval
        try:
            items = validate_records(retrieve())
            if not items:
                raise ProviderError("Provider returned no valid records")

            status = getattr(items[0], "data_status", "live" if provider_name not in {"demo", "failing"} else "demo")

            # Store in memory cache
            self._cache[key] = (now, items, provider_name, status, "primary")

            # Opportunistically persist to DB without blocking or raising on DB error
            if persist:
                self._persist_safe(persist, items)

            return FetchResult(
                items=items,
                source_state="primary",
                data_status=status,
                provider=provider_name,
            )
        except Exception as exc:
            if not isinstance(exc, ProviderError):
                logger.warning(
                    "Provider %s failed (%s); using cache/demo fallback",
                    provider_name,
                    exc.__class__.__name__,
                )
            else:
                logger.warning(
                    "Provider %s failed; using cache/demo fallback",
                    provider_name,
                )

            # 3. Check DB cache if available
            if load_cache:
                cached = self._load_safe(load_cache)
                if cached:
                    for item in cached:
                        if hasattr(item, "data_status"):
                            item.data_status = "cached"
                    return FetchResult(
                        items=cached,
                        source_state="cached",
                        data_status="cached",
                        provider=provider_name,
                    )

            # 4. Check memory cache (stale/cached)
            if key in self._cache:
                _, mem_items, mem_prov, _, _ = self._cache[key]
                if mem_items:
                    cached_copies = []
                    for item in mem_items:
                        item_copy = item.model_copy() if hasattr(item, "model_copy") else item
                        if hasattr(item_copy, "data_status"):
                            item_copy.data_status = "cached"
                        cached_copies.append(item_copy)
                    return FetchResult(
                        items=cached_copies,
                        source_state="cached",
                        data_status="cached",
                        provider=mem_prov,
                    )

            # 5. Fallback to demo catalog
            demo_items = validate_records(fallback())
            for item in demo_items:
                if hasattr(item, "data_status"):
                    item.data_status = "demo"
            return FetchResult(
                items=demo_items,
                source_state="demo_fallback",
                data_status="demo",
                provider="demo",
            )

    def _persist_safe(
        self,
        persist: Callable[[PersistenceRepository, list[T]], None],
        items: list[T],
    ) -> None:
        """Opportunistic persistence that never throws or crashes live request."""
        try:
            session = self._session_factory()
            try:
                persist(PersistenceRepository(session), items)
                session.commit()
            except Exception:
                session.rollback()
            finally:
                session.close()
        except Exception:
            pass

    def _load_safe(
        self,
        load_cache: Callable[[PersistenceRepository], list[T]],
    ) -> list[T]:
        """Safe cache loading that never throws on DB absence."""
        try:
            session = self._session_factory()
            try:
                return load_cache(PersistenceRepository(session))
            except Exception:
                return []
            finally:
                session.close()
        except Exception:
            return []
