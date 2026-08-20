"""Unit and fallback tests for free public live data providers."""

from app.adapters.free_announcements import FreeAnnouncementProvider
from app.adapters.free_geopolitical import FreeGeopoliticalProvider
from app.adapters.free_macro import FreeMacroProvider
from app.adapters.free_market import FreeMarketProvider
from app.adapters.free_news import FreeNewsProvider
from app.adapters.registry import ProviderRegistry
from app.core.config import Settings


def test_free_macro_provider_fallback_and_indicators():
    provider = FreeMacroProvider(timeout_seconds=0.5)
    indicators = provider.list_indicators()
    assert len(indicators) >= 4
    names = [i.indicator for i in indicators]
    assert "CPI Inflation" in names
    assert "Policy Repo Rate" in names

    history = provider.get_indicator_history("CPI Inflation")
    assert len(history) > 0


def test_free_news_provider_classification():
    provider = FreeNewsProvider()
    cat = provider._classify_category("RBI keeps repo rate unchanged amid CPI inflation", "")
    assert cat == "MACRO"
    entities = provider._extract_entities("TCS and Infosys report Q4 revenue growth", "")
    assert "TCS" in entities
    assert "INFY" in entities


def test_free_geopolitical_provider_classification():
    provider = FreeGeopoliticalProvider()
    sev, rel = provider._calculate_scores("Missile strike disrupts Middle East shipping route", "")
    assert sev >= 70
    assert rel >= 70
    cat = provider._classify_category("US imposes new tariff on semiconductor exports", "")
    assert "Tariff" in cat or "Trade" in cat


def test_free_announcements_provider_classification():
    provider = FreeAnnouncementProvider()
    cat = provider._classify_category("Reliance declares final dividend of Rs 10 per share", "")
    assert cat == "CORPORATE_ACTION"
    comp = provider._extract_company("HDFC Bank board meeting scheduled for Q1 results", "")
    assert comp == "HDFCBANK"


def test_registry_live_mode():
    settings = Settings(data_mode="live")
    registry = ProviderRegistry(settings)
    assert isinstance(registry.market_provider, FreeMarketProvider)
    assert isinstance(registry.macro_provider, FreeMacroProvider)
    assert isinstance(registry.news_provider, FreeNewsProvider)
    assert isinstance(registry.geopolitical_provider, FreeGeopoliticalProvider)
    assert isinstance(registry.announcement_provider, FreeAnnouncementProvider)
