"""Deterministic demo market data. Always labeled demo — never live."""

from datetime import datetime, timezone

from app.adapters.demo.catalog import (
    DEMO_AS_OF,
    DEMO_INDICES,
    DEMO_MARKET_SOURCE,
    DEMO_QUOTES,
    generate_demo_history,
)
from app.adapters.interfaces import MarketDataProvider
from app.adapters.normalized import HistoricalPricePoint, MarketIndexRecord, MarketQuote


class DemoMarketProvider(MarketDataProvider):
    name = "demo"
    mode = "demo"

    def capabilities(self) -> list[str]:
        return ["quotes", "indices", "history", "search"]

    def list_quotes(self) -> list[MarketQuote]:
        retrieved = datetime.now(timezone.utc)
        quotes = [
            MarketQuote(
                symbol=row["symbol"],
                name=row["name"],
                price=float(row["price"]),
                change=float(row["change"]),
                change_percent=float(row["change_percent"]),
                volume=int(row["volume"]),
                timestamp=DEMO_AS_OF,
                provider=self.name,
                data_status="demo",
                source=DEMO_MARKET_SOURCE,
                source_url=None,
                sector=row.get("sector"),
                retrieved_at=retrieved,
            )
            for row in DEMO_QUOTES
        ]
        self._tracker.mark_available(self.capabilities())
        return quotes

    def list_indices(self) -> list[MarketIndexRecord]:
        retrieved = datetime.now(timezone.utc)
        indices = [
            MarketIndexRecord(
                symbol=row["symbol"],
                name=row["name"],
                value=float(row["value"]),
                change=float(row["change"]),
                change_percent=float(row["change_percent"]),
                timestamp=DEMO_AS_OF,
                provider=self.name,
                data_status="demo",
                source=DEMO_MARKET_SOURCE,
                retrieved_at=retrieved,
            )
            for row in DEMO_INDICES
        ]
        self._tracker.mark_available(self.capabilities())
        return indices

    def get_history(self, symbol: str, timeframe: str = "1M") -> list[HistoricalPricePoint]:
        target = symbol.upper()
        base_price = 1000.0

        # Check if it's a known equity quote
        for row in DEMO_QUOTES:
            if row["symbol"].upper() == target:
                base_price = float(row["price"])
                break
        else:
            # Check if it's a known index
            for row in DEMO_INDICES:
                if row["symbol"].upper() == target:
                    base_price = float(row["value"])
                    break

        raw_points = generate_demo_history(base_price, timeframe)
        return [
            HistoricalPricePoint(
                timestamp=pt["timestamp"],
                open=pt["open"],
                high=pt["high"],
                low=pt["low"],
                close=pt["close"],
                volume=pt["volume"],
            )
            for pt in raw_points
        ]
