"""SQLite persistence used as the first cache layer."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.adapters.normalized import (
    AnnouncementRecord,
    GeopoliticalRecord,
    MacroRecord,
    MarketIndexRecord,
    MarketQuote,
    NewsRecord,
)
from app.database.models import (
    Announcement,
    GeopoliticalEvent,
    Index,
    MacroIndicator,
    MarketPrice,
    NewsArticle,
)


class PersistenceRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save_quotes(self, quotes: list[MarketQuote]) -> None:
        for quote in quotes:
            existing = self.session.scalar(
                select(MarketPrice).where(MarketPrice.symbol == quote.symbol)
            )
            retrieved = quote.retrieved_at or datetime.now(timezone.utc)
            values = {
                "name": quote.name,
                "price": quote.price,
                "change": quote.change,
                "change_percent": quote.change_percent,
                "volume": quote.volume,
                "timestamp": quote.timestamp,
                "provider": quote.provider,
                "source": quote.source,
                "source_url": quote.source_url,
                "retrieved_at": retrieved,
                "data_status": quote.data_status,
            }
            if existing:
                for key, value in values.items():
                    setattr(existing, key, value)
            else:
                self.session.add(MarketPrice(symbol=quote.symbol, **values))
        self.session.commit()

    def load_quotes(self) -> list[MarketQuote]:
        rows = self.session.scalars(select(MarketPrice)).all()
        return [
            MarketQuote(
                symbol=row.symbol,
                name=row.name,
                price=float(row.price),
                change=float(row.change) if row.change is not None else None,
                change_percent=row.change_percent,
                volume=row.volume,
                timestamp=row.timestamp,
                provider=row.provider,
                data_status="cached",
                source=row.source,
                source_url=row.source_url,
                retrieved_at=row.retrieved_at,
            )
            for row in rows
        ]

    def get_quote_by_symbol(self, symbol: str) -> MarketQuote | None:
        target = symbol.upper()
        row = self.session.scalar(
            select(MarketPrice).where(MarketPrice.symbol == target)
        )
        if not row:
            return None
        return MarketQuote(
            symbol=row.symbol,
            name=row.name,
            price=float(row.price),
            change=float(row.change) if row.change is not None else None,
            change_percent=row.change_percent,
            volume=row.volume,
            timestamp=row.timestamp,
            provider=row.provider,
            data_status="cached",
            source=row.source,
            source_url=row.source_url,
            retrieved_at=row.retrieved_at,
        )

    def save_indices(self, indices: list[MarketIndexRecord]) -> None:
        for idx in indices:
            existing = self.session.scalar(
                select(Index).where(Index.symbol == idx.symbol)
            )
            retrieved = idx.retrieved_at or datetime.now(timezone.utc)
            values = {
                "name": idx.name,
                "value": idx.value,
                "change": idx.change,
                "change_percent": idx.change_percent,
                "timestamp": idx.timestamp,
                "provider": idx.provider,
                "source": idx.source,
                "retrieved_at": retrieved,
                "data_status": idx.data_status,
            }
            if existing:
                for key, value in values.items():
                    setattr(existing, key, value)
            else:
                self.session.add(Index(symbol=idx.symbol, **values))
        self.session.commit()

    def load_indices(self) -> list[MarketIndexRecord]:
        rows = self.session.scalars(select(Index)).all()
        return [
            MarketIndexRecord(
                symbol=row.symbol,
                name=row.name,
                value=float(row.value),
                change=float(row.change) if row.change is not None else None,
                change_percent=row.change_percent,
                timestamp=row.timestamp,
                provider=row.provider,
                data_status="cached",
                source=row.source,
                retrieved_at=row.retrieved_at,
            )
            for row in rows
        ]

    def save_news(self, articles: list[NewsRecord]) -> None:
        for article in articles:
            existing = self.session.scalar(
                select(NewsArticle).where(NewsArticle.headline == article.headline)
            )
            retrieved = article.retrieved_at or datetime.now(timezone.utc)
            values = {
                "summary": article.summary,
                "category": article.category,
                "related_entities": article.related_entities,
                "provider": article.provider,
                "source": article.source,
                "source_url": article.source_url,
                "published_at": article.published_at,
                "retrieved_at": retrieved,
                "data_status": article.data_status,
            }
            if existing:
                for key, value in values.items():
                    setattr(existing, key, value)
            else:
                self.session.add(NewsArticle(headline=article.headline, **values))
        self.session.commit()

    def load_news(self) -> list[NewsRecord]:
        rows = self.session.scalars(select(NewsArticle)).all()
        return [
            NewsRecord(
                headline=row.headline,
                summary=row.summary or "",
                source=row.source or "cached",
                source_url=row.source_url,
                published_at=row.published_at or row.retrieved_at,
                category=row.category or "Markets",
                related_entities=list(row.related_entities or []),
                provider=row.provider,
                data_status="cached",
                retrieved_at=row.retrieved_at,
            )
            for row in rows
        ]

    def save_macro(self, records: list[MacroRecord]) -> None:
        for record in records:
            existing = self.session.scalar(
                select(MacroIndicator).where(MacroIndicator.indicator == record.indicator)
            )
            retrieved = record.retrieved_at or datetime.now(timezone.utc)
            values = {
                "value": record.value,
                "unit": record.unit,
                "period": record.period,
                "previous_value": record.previous_value,
                "change": record.change,
                "provider": record.provider,
                "source": record.source,
                "retrieved_at": retrieved,
                "data_status": record.data_status,
            }
            if existing:
                for key, value in values.items():
                    setattr(existing, key, value)
            else:
                self.session.add(MacroIndicator(indicator=record.indicator, **values))
        self.session.commit()

    def load_macro(self) -> list[MacroRecord]:
        rows = self.session.scalars(select(MacroIndicator)).all()
        return [
            MacroRecord(
                indicator=row.indicator,
                value=float(row.value),
                unit=row.unit or "",
                period=row.period or "",
                previous_value=row.previous_value,
                change=row.change,
                source=row.source or "cached",
                provider=row.provider,
                data_status="cached",
                retrieved_at=row.retrieved_at,
            )
            for row in rows
        ]

    def get_macro_by_indicator(self, name: str) -> MacroRecord | None:
        target = name.strip().lower()
        rows = self.load_macro()
        for r in rows:
            if r.indicator.strip().lower() == target:
                return r
        return None

    def save_events(self, events: list[GeopoliticalRecord]) -> None:
        for event in events:
            existing = self.session.scalar(
                select(GeopoliticalEvent).where(GeopoliticalEvent.title == event.title)
            )
            retrieved = event.retrieved_at or datetime.now(timezone.utc)
            values = {
                "region": event.region,
                "country": event.country,
                "category": event.category,
                "severity": event.severity,
                "event_date": event.event_date,
                "market_relevance": event.market_relevance,
                "related_sectors": event.related_sectors,
                "provider": event.provider,
                "source": event.source,
                "retrieved_at": retrieved,
                "data_status": event.data_status,
            }
            if existing:
                for key, value in values.items():
                    setattr(existing, key, value)
            else:
                self.session.add(GeopoliticalEvent(title=event.title, **values))
        self.session.commit()

    def load_events(self) -> list[GeopoliticalRecord]:
        rows = self.session.scalars(select(GeopoliticalEvent)).all()
        return [
            GeopoliticalRecord(
                title=row.title,
                region=row.region or "",
                country=row.country or "",
                category=row.category or "",
                severity=row.severity or 0,
                event_date=row.event_date or row.retrieved_at,
                market_relevance=row.market_relevance or 0,
                related_sectors=list(row.related_sectors or []),
                provider=row.provider,
                data_status="cached",
                source=row.source,
                retrieved_at=row.retrieved_at,
            )
            for row in rows
        ]

    def save_announcements(self, records: list[AnnouncementRecord]) -> None:
        for record in records:
            existing = self.session.scalar(
                select(Announcement).where(Announcement.title == record.title)
            )
            retrieved = record.retrieved_at or datetime.now(timezone.utc)
            values = {
                "category": record.category,
                "event_date": record.date,
                "importance": record.importance,
                "related_sectors": record.related_sectors,
                "provider": record.provider,
                "source": record.source,
                "source_url": record.source_url,
                "retrieved_at": retrieved,
                "data_status": record.data_status,
            }
            if existing:
                for key, value in values.items():
                    setattr(existing, key, value)
            else:
                self.session.add(Announcement(title=record.title, **values))
        self.session.commit()

    def load_announcements(self) -> list[AnnouncementRecord]:
        rows = self.session.scalars(select(Announcement)).all()
        return [
            AnnouncementRecord(
                title=row.title,
                category=row.category or "",
                date=row.event_date or datetime.now(timezone.utc).date(),
                importance=row.importance or "medium",
                source=row.source or "cached",
                source_url=row.source_url,
                related_sectors=list(row.related_sectors or []),
                provider=row.provider,
                data_status="cached",
                retrieved_at=row.retrieved_at,
            )
            for row in rows
        ]
