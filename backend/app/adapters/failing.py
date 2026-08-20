"""Providers that always fail, used to test fallback without crashing."""

from app.adapters.exceptions import ProviderError
from app.adapters.interfaces import (
    AnnouncementProvider,
    GeopoliticalProvider,
    MacroDataProvider,
    MarketDataProvider,
    NewsProvider,
)
from app.adapters.normalized import (
    AnnouncementRecord,
    GeopoliticalRecord,
    HistoricalPricePoint,
    MacroHistoryPoint,
    MacroRecord,
    MarketIndexRecord,
    MarketQuote,
    NewsRecord,
)


class FailingMarketProvider(MarketDataProvider):
    name = "failing"
    mode = "error"

    def capabilities(self) -> list[str]:
        return ["quotes", "indices", "history", "search"]

    def list_quotes(self) -> list[MarketQuote]:
        message = "Intentional failure for fallback testing"
        self._tracker.mark_error(message)
        raise ProviderError(message)

    def list_indices(self) -> list[MarketIndexRecord]:
        message = "Intentional failure for fallback testing"
        self._tracker.mark_error(message)
        raise ProviderError(message)

    def get_history(self, symbol: str, timeframe: str = "1M") -> list[HistoricalPricePoint]:
        message = "Intentional failure for fallback testing"
        self._tracker.mark_error(message)
        raise ProviderError(message)


class FailingNewsProvider(NewsProvider):
    name = "failing"
    mode = "error"

    def list_articles(self) -> list[NewsRecord]:
        message = "Intentional failure for fallback testing"
        self._tracker.mark_error(message)
        raise ProviderError(message)


class FailingMacroProvider(MacroDataProvider):
    name = "failing"
    mode = "error"

    def list_indicators(self) -> list[MacroRecord]:
        message = "Intentional failure for fallback testing"
        self._tracker.mark_error(message)
        raise ProviderError(message)

    def get_indicator_history(self, name: str) -> list[MacroHistoryPoint]:
        message = "Intentional failure for fallback testing"
        self._tracker.mark_error(message)
        raise ProviderError(message)


class FailingGeopoliticalProvider(GeopoliticalProvider):
    name = "failing"
    mode = "error"

    def list_events(self) -> list[GeopoliticalRecord]:
        message = "Intentional failure for fallback testing"
        self._tracker.mark_error(message)
        raise ProviderError(message)


class FailingAnnouncementProvider(AnnouncementProvider):
    name = "failing"
    mode = "error"

    def list_announcements(self) -> list[AnnouncementRecord]:
        message = "Intentional failure for fallback testing"
        self._tracker.mark_error(message)
        raise ProviderError(message)
