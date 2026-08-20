"""Deterministic demo announcements. No real government or regulator URLs."""

from datetime import datetime, timezone

from app.adapters.demo.catalog import DEMO_ANNOUNCEMENT_SOURCE, DEMO_ANNOUNCEMENTS
from app.adapters.interfaces import AnnouncementProvider
from app.adapters.normalized import AnnouncementRecord


class DemoAnnouncementProvider(AnnouncementProvider):
    name = "demo"
    mode = "demo"

    def capabilities(self) -> list[str]:
        return ["announcements", "categories"]

    def list_announcements(self) -> list[AnnouncementRecord]:
        retrieved = datetime.now(timezone.utc)
        records = [
            AnnouncementRecord(
                id=row.get("id"),
                title=row["title"],
                category=row["category"],
                announcement_type=row.get("announcement_type", "ANNOUNCEMENT"),
                date=row["date"],
                importance=row["importance"],
                source=DEMO_ANNOUNCEMENT_SOURCE,
                source_url=None,
                related_sectors=list(row.get("related_sectors", [])),
                related_entities=list(row.get("related_entities", [])),
                provider=self.name,
                data_status="demo",
                retrieved_at=retrieved,
            )
            for row in DEMO_ANNOUNCEMENTS
        ]
        self._tracker.mark_available(self.capabilities())
        return records
