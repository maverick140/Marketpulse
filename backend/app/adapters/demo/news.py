"""Deterministic demo news. Source is Demo Research Feed — never live news."""

from datetime import datetime, timezone

from app.adapters.demo.catalog import DEMO_AS_OF, DEMO_NEWS, DEMO_SOURCE
from app.adapters.interfaces import NewsProvider
from app.adapters.normalized import NewsRecord


class DemoNewsProvider(NewsProvider):
    name = "demo"
    mode = "demo"

    def capabilities(self) -> list[str]:
        return ["articles", "search", "categories"]

    def list_articles(self) -> list[NewsRecord]:
        retrieved = datetime.now(timezone.utc)
        articles: list[NewsRecord] = []
        for row in DEMO_NEWS:
            item = NewsRecord(
                id=row.get("id"),
                headline=row["headline"],
                summary=row["summary"],
                source=DEMO_SOURCE,
                source_url=None,
                published_at=DEMO_AS_OF,
                category=row["category"],
                related_entities=list(row.get("related_entities", [])),
                related_sectors=list(row.get("related_sectors", [])),
                countries=list(row.get("countries", [])),
                language=row.get("language", "en"),
                author=row.get("author"),
                provider=self.name,
                data_status="demo",
                retrieved_at=retrieved,
            )
            item.content_hash = item.compute_hash()
            articles.append(item)
        self._tracker.mark_available(self.capabilities())
        return articles
