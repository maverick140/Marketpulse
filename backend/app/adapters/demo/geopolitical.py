"""Deterministic demo geopolitical events. Always labeled demo."""

from datetime import datetime, timezone

from app.adapters.demo.catalog import DEMO_AS_OF, DEMO_EVENTS, DEMO_GEO_SOURCE
from app.adapters.interfaces import GeopoliticalProvider
from app.adapters.normalized import GeopoliticalRecord


class DemoGeopoliticalProvider(GeopoliticalProvider):
    name = "demo"
    mode = "demo"

    def capabilities(self) -> list[str]:
        return ["events", "regions", "severity"]

    def list_events(self) -> list[GeopoliticalRecord]:
        retrieved = datetime.now(timezone.utc)
        events = [
            GeopoliticalRecord(
                id=row.get("id"),
                title=row["title"],
                description=row.get("description"),
                region=row["region"],
                country=row["country"],
                category=row["category"],
                severity=int(row["severity"]),
                event_date=DEMO_AS_OF,
                market_relevance=int(row["market_relevance"]),
                related_sectors=list(row.get("related_sectors", [])),
                affected_assets=list(row.get("affected_assets", [])),
                provider=self.name,
                data_status="demo",
                source=DEMO_GEO_SOURCE,
                retrieved_at=retrieved,
            )
            for row in DEMO_EVENTS
        ]
        self._tracker.mark_available(self.capabilities())
        return events
