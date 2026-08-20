"""Tests for market and macro gateway fallback behavior."""

from app.adapters.demo.macro import DemoMacroProvider
from app.adapters.demo.market import DemoMarketProvider
from app.adapters.failing import FailingMacroProvider, FailingMarketProvider
from app.adapters.gateway import DataGateway
from app.database.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import models as _models  # noqa: F401


def _session_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


def test_market_overview_fallback() -> None:
    factory = _session_factory()
    gateway = DataGateway(session_factory=factory)
    failing = FailingMarketProvider()
    demo = DemoMarketProvider()

    res = gateway.fetch(
        provider_name="failing",
        retrieve=failing.list_quotes,
        persist=lambda repo, items: repo.save_quotes(items),
        load_cache=lambda repo: repo.load_quotes(),
        fallback=demo.list_quotes,
    )
    assert res.source_state == "demo_fallback"
    assert res.data_status == "demo"
    assert len(res.items) >= 10


def test_macro_indicators_fallback() -> None:
    factory = _session_factory()
    gateway = DataGateway(session_factory=factory)
    failing = FailingMacroProvider()
    demo = DemoMacroProvider()

    res = gateway.fetch(
        provider_name="failing",
        retrieve=failing.list_indicators,
        persist=lambda repo, items: repo.save_macro(items),
        load_cache=lambda repo: repo.load_macro(),
        fallback=demo.list_indicators,
    )
    assert res.source_state == "demo_fallback"
    assert res.data_status == "demo"
    assert len(res.items) >= 7
