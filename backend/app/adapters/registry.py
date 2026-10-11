"""Select providers from configuration. Defaults to demo; no API keys required."""

from __future__ import annotations

from functools import lru_cache

from app.adapters.demo.announcements import DemoAnnouncementProvider
from app.adapters.demo.geopolitical import DemoGeopoliticalProvider
from app.adapters.demo.macro import DemoMacroProvider
from app.adapters.demo.market import DemoMarketProvider
from app.adapters.demo.news import DemoNewsProvider
from app.adapters.failing import (
    FailingAnnouncementProvider,
    FailingGeopoliticalProvider,
    FailingMacroProvider,
    FailingMarketProvider,
    FailingNewsProvider,
)
from app.adapters.free_announcements import FreeAnnouncementProvider
from app.adapters.free_geopolitical import FreeGeopoliticalProvider
from app.adapters.free_macro import FreeMacroProvider
from app.adapters.free_market import FreeMarketProvider
from app.adapters.free_news import FreeNewsProvider
from app.adapters.gateway import DataGateway
from app.adapters.interfaces import (
    AnnouncementProvider,
    GeopoliticalProvider,
    MacroDataProvider,
    MarketDataProvider,
    NewsProvider,
)
from app.adapters.status import ProviderStatus
from app.core.config import Settings, get_settings
from app.core.logging_config import get_logger

logger = get_logger("registry")

MARKET_FACTORIES = {
    "demo": DemoMarketProvider,
    "failing": FailingMarketProvider,
    "free": FreeMarketProvider,
    "live": FreeMarketProvider,
}
NEWS_FACTORIES = {
    "demo": DemoNewsProvider,
    "failing": FailingNewsProvider,
    "free": FreeNewsProvider,
    "live": FreeNewsProvider,
}
MACRO_FACTORIES = {
    "demo": DemoMacroProvider,
    "failing": FailingMacroProvider,
    "free": FreeMacroProvider,
    "live": FreeMacroProvider,
}
GEO_FACTORIES = {
    "demo": DemoGeopoliticalProvider,
    "failing": FailingGeopoliticalProvider,
    "free": FreeGeopoliticalProvider,
    "live": FreeGeopoliticalProvider,
}
ANNOUNCEMENT_FACTORIES = {
    "demo": DemoAnnouncementProvider,
    "failing": FailingAnnouncementProvider,
    "free": FreeAnnouncementProvider,
    "live": FreeAnnouncementProvider,
}


def resolve_provider_name(configured: str, data_mode: str) -> str:
    name = (configured or "").strip().lower()
    if data_mode.lower() in {"live", "free"}:
        if name in {"failing"}:
            return name
        return "free"
    if name in {"free", "live", "demo", "failing"}:
        return name
    return "demo"


def _build(name: str, factories: dict, fallback_factory):
    factory = factories.get(name)
    if factory is None:
        logger.warning("Unknown provider '%s'; using demo", name)
        return fallback_factory()
    return factory()


class ProviderRegistry:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        data_mode = self.settings.data_mode
        self.market_provider: MarketDataProvider = _build(
            resolve_provider_name(self.settings.market_provider, data_mode),
            MARKET_FACTORIES,
            DemoMarketProvider,
        )
        self.news_provider: NewsProvider = _build(
            resolve_provider_name(self.settings.news_provider, data_mode),
            NEWS_FACTORIES,
            DemoNewsProvider,
        )
        self.macro_provider: MacroDataProvider = _build(
            resolve_provider_name(self.settings.macro_provider, data_mode),
            MACRO_FACTORIES,
            DemoMacroProvider,
        )
        self.geopolitical_provider: GeopoliticalProvider = _build(
            resolve_provider_name(self.settings.geopolitical_provider, data_mode),
            GEO_FACTORIES,
            DemoGeopoliticalProvider,
        )
        self.announcement_provider: AnnouncementProvider = _build(
            resolve_provider_name(self.settings.announcement_provider, data_mode),
            ANNOUNCEMENT_FACTORIES,
            DemoAnnouncementProvider,
        )
        self.gateway = DataGateway()

    def statuses(self) -> list[ProviderStatus]:
        return [
            self.market_provider.get_status(),
            self.news_provider.get_status(),
            self.macro_provider.get_status(),
            self.geopolitical_provider.get_status(),
            self.announcement_provider.get_status(),
        ]


@lru_cache
def get_registry() -> ProviderRegistry:
    return ProviderRegistry()
