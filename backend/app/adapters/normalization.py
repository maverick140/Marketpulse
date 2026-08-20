"""Map provider-specific dictionaries into internal records."""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

from app.adapters.normalized import (
    AnnouncementRecord,
    GeopoliticalRecord,
    MacroRecord,
    MarketIndexRecord,
    MarketQuote,
    NewsRecord,
)


def _as_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day, tzinfo=timezone.utc)
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed
    return datetime.now(timezone.utc)


def _as_date(value: Any) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value[:10])
    return datetime.now(timezone.utc).date()


def _first(raw: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in raw and raw[key] is not None:
            return raw[key]
    return None


def normalize_market_quote(raw: dict[str, Any], *, default_provider: str = "unknown") -> MarketQuote:
    retrieved = _as_datetime(_first(raw, "retrieved_at")) if _first(raw, "retrieved_at") else datetime.now(timezone.utc)
    timestamp = _first(raw, "timestamp", "as_of", "time")
    return MarketQuote(
        symbol=str(_first(raw, "symbol", "ticker", "code")).upper(),
        name=str(_first(raw, "name", "company", "shortName") or _first(raw, "symbol", "ticker")),
        price=float(_first(raw, "price", "last", "close", "regularMarketPrice")),
        change=_optional_float(_first(raw, "change", "net_change")),
        change_percent=_optional_float(_first(raw, "change_percent", "percent_change", "changePercent")),
        volume=_optional_int(_first(raw, "volume", "regularMarketVolume")),
        timestamp=_as_datetime(timestamp) if timestamp else retrieved,
        provider=str(_first(raw, "provider") or default_provider),
        data_status=str(_first(raw, "data_status", "status") or "demo"),
        source=_optional_str(_first(raw, "source")),
        source_url=_optional_str(_first(raw, "source_url", "url")),
        retrieved_at=retrieved,
    )


def normalize_news(raw: dict[str, Any], *, default_provider: str = "unknown") -> NewsRecord:
    retrieved = datetime.now(timezone.utc)
    entities = _first(raw, "related_entities", "entities", "tickers") or []
    if isinstance(entities, str):
        entities = [item.strip() for item in entities.split(",") if item.strip()]
    return NewsRecord(
        headline=str(_first(raw, "headline", "title")),
        summary=str(_first(raw, "summary", "description", "body") or ""),
        source=str(_first(raw, "source", "publisher") or "Demo Research Feed"),
        source_url=_optional_str(_first(raw, "source_url", "url", "link")),
        published_at=_as_datetime(_first(raw, "published_at", "published", "date")),
        category=str(_first(raw, "category", "section") or "Markets"),
        related_entities=list(entities),
        provider=str(_first(raw, "provider") or default_provider),
        data_status=str(_first(raw, "data_status") or "demo"),
        retrieved_at=retrieved,
    )


def normalize_macro(raw: dict[str, Any], *, default_provider: str = "unknown") -> MacroRecord:
    return MacroRecord(
        indicator=str(_first(raw, "indicator", "name", "series")),
        value=float(_first(raw, "value", "latest")),
        unit=str(_first(raw, "unit") or ""),
        period=str(_first(raw, "period", "as_of") or ""),
        previous_value=_optional_float(_first(raw, "previous_value", "previous")),
        change=_optional_float(_first(raw, "change")),
        source=str(_first(raw, "source") or "Demo Macro Catalog"),
        provider=str(_first(raw, "provider") or default_provider),
        data_status=str(_first(raw, "data_status") or "demo"),
        retrieved_at=datetime.now(timezone.utc),
    )


def normalize_geopolitical(raw: dict[str, Any], *, default_provider: str = "unknown") -> GeopoliticalRecord:
    sectors = _first(raw, "related_sectors", "sectors") or []
    return GeopoliticalRecord(
        title=str(_first(raw, "title", "event", "headline")),
        region=str(_first(raw, "region") or ""),
        country=str(_first(raw, "country") or ""),
        category=str(_first(raw, "category") or ""),
        severity=int(_first(raw, "severity") or 0),
        event_date=_as_datetime(_first(raw, "event_date", "date")),
        market_relevance=int(_first(raw, "market_relevance", "relevance") or 0),
        related_sectors=list(sectors),
        provider=str(_first(raw, "provider") or default_provider),
        data_status=str(_first(raw, "data_status") or "demo"),
        source=_optional_str(_first(raw, "source")),
        retrieved_at=datetime.now(timezone.utc),
    )


def normalize_announcement(raw: dict[str, Any], *, default_provider: str = "unknown") -> AnnouncementRecord:
    sectors = _first(raw, "related_sectors", "sectors") or []
    return AnnouncementRecord(
        title=str(_first(raw, "title", "headline")),
        category=str(_first(raw, "category") or ""),
        date=_as_date(_first(raw, "date", "event_date")),
        importance=str(_first(raw, "importance") or "medium"),
        source=str(_first(raw, "source") or "Demo Announcement Catalog"),
        source_url=_optional_str(_first(raw, "source_url", "url")),
        related_sectors=list(sectors),
        provider=str(_first(raw, "provider") or default_provider),
        data_status=str(_first(raw, "data_status") or "demo"),
        retrieved_at=datetime.now(timezone.utc),
    )


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _optional_str(value: Any) -> str | None:
    if value is None or value == "":
        return None
    return str(value)
