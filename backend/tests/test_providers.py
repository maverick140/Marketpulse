"""Demo provider tests."""

from app.adapters.demo.announcements import DemoAnnouncementProvider
from app.adapters.demo.catalog import DEMO_QUOTES
from app.adapters.demo.geopolitical import DemoGeopoliticalProvider
from app.adapters.demo.macro import DemoMacroProvider
from app.adapters.demo.market import DemoMarketProvider
from app.adapters.demo.news import DemoNewsProvider


def test_demo_market_provider() -> None:
    provider = DemoMarketProvider()
    quotes = provider.list_quotes()
    indices = provider.list_indices()
    symbols = {row.symbol for row in quotes}
    expected = {row["symbol"] for row in DEMO_QUOTES}
    assert symbols == expected
    assert {row.symbol for row in indices} >= {"NIFTY 50", "SENSEX", "NIFTY BANK", "NIFTY IT"}
    assert all(row.data_status == "demo" for row in quotes)
    assert all(row.provider == "demo" for row in quotes)
    assert all(row.data_status == "demo" for row in indices)
    reliance = provider.get_quote("RELIANCE")
    assert reliance is not None
    assert reliance.price > 0
    status = provider.get_status()
    assert status.status == "available"
    assert status.mode == "demo"
    assert "quotes" in status.capabilities


def test_demo_news_provider() -> None:
    articles = DemoNewsProvider().list_articles()
    assert len(articles) >= 4
    assert all(item.data_status == "demo" for item in articles)
    assert all(item.source == "Demo Research Feed" for item in articles)
    assert all(item.source_url is None for item in articles)
    assert all(item.headline.startswith("Demo:") for item in articles)


def test_demo_macro_provider() -> None:
    records = DemoMacroProvider().list_indicators()
    names = {row.indicator for row in records}
    assert names >= {
        "Inflation",
        "Interest Rate",
        "GDP Growth",
        "Unemployment",
        "Oil",
        "Gold",
        "Currency",
    }
    assert all(row.data_status == "demo" for row in records)
    assert all(row.provider == "demo" for row in records)


def test_demo_geopolitical_provider() -> None:
    events = DemoGeopoliticalProvider().list_events()
    assert len(events) >= 4
    assert all(row.data_status == "demo" for row in events)
    assert {row.category for row in events} >= {"Trade", "Energy", "Regulation", "Diplomacy"}
    assert all(row.title.startswith("Demo:") for row in events)


def test_demo_announcement_provider() -> None:
    records = DemoAnnouncementProvider().list_announcements()
    assert len(records) >= 4
    assert all(row.data_status == "demo" for row in records)
    assert all(row.source_url is None for row in records)
    assert all(row.title.startswith("Demo:") for row in records)
