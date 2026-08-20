"""Provider registry and selection tests."""

from app.adapters.demo.market import DemoMarketProvider
from app.adapters.failing import FailingMarketProvider
from app.adapters.registry import ProviderRegistry, resolve_provider_name
from app.core.config import Settings


def test_resolve_provider_name_defaults_to_demo() -> None:
    assert resolve_provider_name("", "demo") == "demo"
    assert resolve_provider_name("failing", "demo") == "failing"


def test_registry_selects_demo_providers() -> None:
    registry = ProviderRegistry(Settings(data_mode="demo"))
    assert isinstance(registry.market_provider, DemoMarketProvider)
    assert registry.news_provider.name == "demo"
    assert registry.macro_provider.name == "demo"
    assert registry.geopolitical_provider.name == "demo"
    assert registry.announcement_provider.name == "demo"
    types = {item.type for item in registry.statuses()}
    assert types == {"market", "news", "macro", "geopolitical", "announcement"}
    assert all(item.mode == "demo" for item in registry.statuses())
    assert all(item.status == "available" for item in registry.statuses())


def test_registry_can_select_failing_market_provider() -> None:
    registry = ProviderRegistry(Settings(market_provider="failing", data_mode="demo"))
    assert isinstance(registry.market_provider, FailingMarketProvider)
    assert registry.news_provider.name == "demo"


def test_unknown_provider_falls_back_to_demo() -> None:
    registry = ProviderRegistry(Settings(market_provider="not-a-real-provider"))
    assert isinstance(registry.market_provider, DemoMarketProvider)
