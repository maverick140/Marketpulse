"""Provider interfaces (abstract base classes)."""

from __future__ import annotations

from abc import ABC, abstractmethod

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
from app.adapters.status import ProviderStatus, StatusTracker


class BaseProvider(ABC):
    name: str
    provider_type: str
    mode: str = "demo"

    def __init__(self) -> None:
        self._tracker = StatusTracker(self.name, self.provider_type, self.mode)
        self._tracker.capabilities = list(self.capabilities())
        if self.mode == "demo":
            self._tracker.status = "available"

    def capabilities(self) -> list[str]:
        return []

    def get_status(self) -> ProviderStatus:
        return self._tracker.snapshot()


class MarketDataProvider(BaseProvider):
    provider_type = "market"

    @abstractmethod
    def list_quotes(self) -> list[MarketQuote]:
        raise NotImplementedError

    @abstractmethod
    def list_indices(self) -> list[MarketIndexRecord]:
        raise NotImplementedError

    def get_quote(self, symbol: str) -> MarketQuote | None:
        target = symbol.upper()
        for quote in self.list_quotes():
            if quote.symbol.upper() == target:
                return quote
        return None

    def get_history(self, symbol: str, timeframe: str = "1M") -> list[HistoricalPricePoint]:
        return []

    def search(self, query: str) -> list[MarketQuote]:
        q = (query or "").strip().upper()
        if not q:
            return self.list_quotes()
        return [
            quote for quote in self.list_quotes()
            if q in quote.symbol.upper()
            or q in quote.name.upper()
            or (quote.sector and q in quote.sector.upper())
        ]


class NewsProvider(BaseProvider):
    provider_type = "news"

    @abstractmethod
    def list_articles(self) -> list[NewsRecord]:
        raise NotImplementedError


class MacroDataProvider(BaseProvider):
    provider_type = "macro"

    @abstractmethod
    def list_indicators(self) -> list[MacroRecord]:
        raise NotImplementedError

    def get_indicator(self, name: str) -> MacroRecord | None:
        target = name.strip().lower()
        for ind in self.list_indicators():
            if ind.indicator.strip().lower() == target:
                return ind
        return None

    def get_indicator_history(self, name: str) -> list[MacroHistoryPoint]:
        return []


class GeopoliticalProvider(BaseProvider):
    provider_type = "geopolitical"

    @abstractmethod
    def list_events(self) -> list[GeopoliticalRecord]:
        raise NotImplementedError


class AnnouncementProvider(BaseProvider):
    provider_type = "announcement"

    @abstractmethod
    def list_announcements(self) -> list[AnnouncementRecord]:
        raise NotImplementedError
