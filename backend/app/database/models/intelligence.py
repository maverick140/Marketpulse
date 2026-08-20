"""News, geopolitics, macro, and research domain models."""

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base
from app.database.models.mixins import ExternalDataMixin, TimestampMixin


class NewsArticle(TimestampMixin, ExternalDataMixin, Base):
    __tablename__ = "news_articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    headline: Mapped[str] = mapped_column(String(512), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    related_entities: Mapped[list] = mapped_column(JSON, default=list, nullable=False)


class SentimentResult(TimestampMixin, ExternalDataMixin, Base):
    __tablename__ = "sentiment_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    news_article_id: Mapped[int | None] = mapped_column(
        ForeignKey("news_articles.id"), nullable=True
    )
    label: Mapped[str] = mapped_column(String(32), nullable=False)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)


class Country(TimestampMixin, Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    region: Mapped[str | None] = mapped_column(String(64), nullable=True)
    iso_code: Mapped[str | None] = mapped_column(String(8), unique=True, nullable=True)


class GeopoliticalEvent(TimestampMixin, ExternalDataMixin, Base):
    __tablename__ = "geopolitical_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    region: Mapped[str | None] = mapped_column(String(64), nullable=True)
    country: Mapped[str | None] = mapped_column(String(128), nullable=True)
    category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    severity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    event_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    market_relevance: Mapped[int | None] = mapped_column(Integer, nullable=True)
    related_sectors: Mapped[list] = mapped_column(JSON, default=list, nullable=False)


class Announcement(TimestampMixin, ExternalDataMixin, Base):
    __tablename__ = "announcements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    event_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    importance: Mapped[str | None] = mapped_column(String(32), nullable=True)
    related_sectors: Mapped[list] = mapped_column(JSON, default=list, nullable=False)


class MacroIndicator(TimestampMixin, ExternalDataMixin, Base):
    __tablename__ = "macro_indicators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    indicator: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str | None] = mapped_column(String(32), nullable=True)
    period: Mapped[str | None] = mapped_column(String(32), nullable=True)
    previous_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    change: Mapped[float | None] = mapped_column(Float, nullable=True)


class AIInsight(TimestampMixin, ExternalDataMixin, Base):
    __tablename__ = "ai_insights"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    insight: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    uncertainty: Mapped[str | None] = mapped_column(String(32), nullable=True)
    risk_flags: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    sources: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
