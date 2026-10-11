"""Deterministic demo macroeconomic indicators. Always labeled demo."""

from datetime import datetime, timezone

from app.adapters.demo.catalog import (
    DEMO_MACRO,
    DEMO_MACRO_HISTORY,
    DEMO_MACRO_SOURCE,
)
from app.adapters.interfaces import MacroDataProvider
from app.adapters.normalized import MacroHistoryPoint, MacroRecord


class DemoMacroProvider(MacroDataProvider):
    name = "demo"
    mode = "demo"

    def capabilities(self) -> list[str]:
        return ["indicators", "history"]

    def list_indicators(self) -> list[MacroRecord]:
        retrieved = datetime.now(timezone.utc)
        records = [
            MacroRecord(
                indicator=row["indicator"],
                value=float(row["value"]),
                unit=row["unit"],
                period=row["period"],
                previous_value=row["previous_value"],
                change=row["change"],
                source=DEMO_MACRO_SOURCE,
                provider=self.name,
                data_status="demo",
                retrieved_at=retrieved,
            )
            for row in DEMO_MACRO
        ]
        self._tracker.mark_available(self.capabilities())
        return records

    def get_indicator(self, name: str) -> MacroRecord | None:
        target = name.strip().lower()
        for ind in self.list_indicators():
            if ind.indicator.strip().lower() == target:
                return ind
        return None

    def get_indicator_history(self, name: str) -> list[MacroHistoryPoint]:
        target = name.strip().lower()
        history_data = DEMO_MACRO_HISTORY.get(target, [])
        return [
            MacroHistoryPoint(
                period=row["period"],
                value=float(row["value"]),
                date=row.get("date"),
            )
            for row in history_data
        ]
