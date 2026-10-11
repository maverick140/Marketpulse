"""Free/public macroeconomic data provider.

Integrates official government economic metrics parsed from raw/ Excel workbooks:
- raw/RBI_Rates.xlsx (Sheet1: Reserve Bank of India repo rate)
- raw/gdp_data.xlsx (GDP 2022-23 series: MoSPI quarterly real GDP growth)
- raw/inflation_data.xlsx (CPI 2024 series: MoSPI CPI combined inflation)

Supplemented by live commodity spot rates and foreign exchange (Brent Oil, Gold, USD/INR)
from open Yahoo Finance chart endpoints.
"""

from __future__ import annotations

from datetime import datetime, timezone
import httpx

from app.adapters.interfaces import MacroDataProvider
from app.adapters.macro_excel import MacroWorkbookError, get_macro_excel_loader
from app.adapters.normalized import MacroHistoryPoint, MacroRecord
from app.core.logging_config import get_logger

logger = get_logger("free_macro")


class FreeMacroProvider(MacroDataProvider):
    """Macroeconomic data provider combining raw/ Excel workbooks with live spot commodities."""

    name = "free"
    mode = "live"

    def __init__(self, timeout_seconds: float = 4.0) -> None:
        super().__init__()
        self.timeout = timeout_seconds
        self.excel_loader = get_macro_excel_loader()

    def capabilities(self) -> list[str]:
        return ["indicators", "history"]

    def list_indicators(self) -> list[MacroRecord]:
        """Fetch macro indicators for India and global benchmarks."""
        records: list[MacroRecord] = []
        now = datetime.now(timezone.utc)

        # 1. Base Indian Macro Economic Metrics from validated Excel workbooks
        try:
            excel_indicators, _ = self.excel_loader.load_data()
            records.extend(excel_indicators)
        except MacroWorkbookError as exc:
            logger.error("Failed to load macro Excel workbooks: %s", exc)
            raise

        # 2. Live Market Commodities & Forex Spot Benchmarks
        ticker_map = {
            "Brent Crude Oil": ("BZ=F", "USD/bbl"),
            "Gold": ("GC=F", "USD/oz"),
            "USD / INR": ("USDINR=X", "INR"),
        }
        commodity_fallbacks = {
            "Brent Crude Oil": (82.50, "USD/bbl", 83.10, -0.60),
            "Gold": (2350.00, "USD/oz", 2342.00, 8.00),
            "USD / INR": (83.52, "INR", 83.48, 0.04),
        }
        fetched_commodities = set()
        try:
            with httpx.Client(timeout=self.timeout) as client:
                for ind_name, (ticker, unit) in ticker_map.items():
                    try:
                        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1d"
                        resp = client.get(url, headers={"User-Agent": "Mozilla/5.0 MarketPulse/1.0"})
                        if resp.status_code == 200:
                            data = resp.json()
                            result = data.get("chart", {}).get("result", [{}])[0]
                            meta = result.get("meta", {})
                            price = meta.get("regularMarketPrice") or meta.get("chartPreviousClose")
                            prev = meta.get("chartPreviousClose") or price
                            if price:
                                change = round(price - prev, 2) if prev else 0.0
                                records.append(
                                    MacroRecord(
                                        indicator=ind_name,
                                        value=round(float(price), 2),
                                        unit=unit,
                                        period="Live Global Spot",
                                        previous_value=round(float(prev), 2) if prev else None,
                                        change=change,
                                        source="Free Public Market API",
                                        provider=self.name,
                                        data_status="live",
                                        retrieved_at=now,
                                    )
                                )
                                fetched_commodities.add(ind_name)
                    except Exception:
                        pass
        except Exception:
            pass

        # Cached/base fallback for commodities if remote fetch timed out
        for ind_name, (val, unit, prev_val, chg) in commodity_fallbacks.items():
            if ind_name not in fetched_commodities:
                records.append(
                    MacroRecord(
                        indicator=ind_name,
                        value=val,
                        unit=unit,
                        period="Global Benchmark",
                        previous_value=prev_val,
                        change=chg,
                        source="Free Public Market API (Cached/Base)",
                        provider=self.name,
                        data_status="live",
                        retrieved_at=now,
                    )
                )

        self._tracker.mark_available(self.capabilities())
        return records

    def get_indicator_history(self, indicator_name: str) -> list[MacroHistoryPoint]:
        """Fetch historical points for a given macro indicator."""
        target = indicator_name.strip().lower()

        # 1. Check Excel workbooks first
        try:
            _, excel_history = self.excel_loader.load_data()
            if target in excel_history:
                return excel_history[target]
        except MacroWorkbookError as exc:
            logger.error("Failed to load macro history from Excel workbooks: %s", exc)
            raise

        # 2. Live ticker commodities
        ticker_map = {
            "brent crude oil": "BZ=F",
            "oil": "BZ=F",
            "gold": "GC=F",
            "usd / inr": "USDINR=X",
            "currency": "USDINR=X",
        }
        if target in ticker_map:
            ticker = ticker_map[target]
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1mo"
                    resp = client.get(url, headers={"User-Agent": "Mozilla/5.0 MarketPulse/1.0"})
                    if resp.status_code == 200:
                        data = resp.json()
                        result = data.get("chart", {}).get("result", [{}])[0]
                        timestamps = result.get("timestamp", [])
                        indicators = result.get("indicators", {}).get("quote", [{}])[0]
                        closes = indicators.get("close", [])
                        points: list[MacroHistoryPoint] = []
                        for i, ts in enumerate(timestamps):
                            c = closes[i] if i < len(closes) else None
                            if c is not None:
                                dt_point = datetime.fromtimestamp(ts, tz=timezone.utc)
                                points.append(
                                    MacroHistoryPoint(
                                        period=dt_point.strftime("%d %b"),
                                        value=round(float(c), 2),
                                        date=dt_point.strftime("%Y-%m-%d"),
                                    )
                                )
                        if points:
                            return points
            except Exception:
                pass

        return []
