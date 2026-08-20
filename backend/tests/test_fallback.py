"""Fallback and failure-handling tests."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.adapters.demo.market import DemoMarketProvider
from app.adapters.exceptions import ProviderError
from app.adapters.failing import FailingMarketProvider
from app.adapters.gateway import DataGateway
from app.database.database import Base
from app.database import models as _models  # noqa: F401


def _session_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


def test_failing_provider_raises_without_crashing_callers() -> None:
    provider = FailingMarketProvider()
    try:
        provider.list_quotes()
        raise AssertionError("expected ProviderError")
    except ProviderError:
        status = provider.get_status()
        assert status.status == "error"
        assert status.last_error is not None
        assert "key" not in status.last_error.lower()


def test_gateway_falls_back_to_demo_when_primary_fails() -> None:
    factory = _session_factory()
    gateway = DataGateway(session_factory=factory)
    failing = FailingMarketProvider()
    demo = DemoMarketProvider()
    result = gateway.fetch(
        provider_name="failing",
        retrieve=failing.list_quotes,
        persist=lambda repo, items: repo.save_quotes(items),
        load_cache=lambda repo: repo.load_quotes(),
        fallback=demo.list_quotes,
    )
    assert result.source_state == "demo_fallback"
    assert result.data_status == "demo"
    assert result.provider == "demo"
    assert len(result.items) >= 10
    assert all(item.data_status == "demo" for item in result.items)


def test_gateway_uses_cache_before_demo_fallback() -> None:
    factory = _session_factory()
    gateway = DataGateway(session_factory=factory)
    demo = DemoMarketProvider()
    first = gateway.fetch(
        provider_name="demo",
        retrieve=demo.list_quotes,
        persist=lambda repo, items: repo.save_quotes(items),
        load_cache=lambda repo: repo.load_quotes(),
        fallback=demo.list_quotes,
    )
    assert first.source_state == "primary"
    failing = FailingMarketProvider()
    second = gateway.fetch(
        provider_name="failing",
        retrieve=failing.list_quotes,
        persist=lambda repo, items: repo.save_quotes(items),
        load_cache=lambda repo: repo.load_quotes(),
        fallback=demo.list_quotes,
    )
    assert second.source_state == "cached"
    assert second.data_status == "cached"
    assert len(second.items) == len(first.items)
