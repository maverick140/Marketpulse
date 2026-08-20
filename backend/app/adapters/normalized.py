"""Normalized internal records shared by all providers."""

from __future__ import annotations

import datetime as dt
import hashlib
from typing import Any, Literal

from pydantic import BaseModel, Field

DataStatus = Literal["demo", "cached", "live", "latest", "historical", "demo_fallback"]
SourceState = Literal["primary", "cached", "demo_fallback"]


class Provenance(BaseModel):
    provider: str
    source: str | None = None
    source_url: str | None = None
    published_at: dt.datetime | None = None
    retrieved_at: dt.datetime
    data_status: str = "demo"


class HistoricalPricePoint(BaseModel):
    timestamp: dt.datetime
    open: float
    high: float
    low: float
    close: float
    volume: int = 0


class MacroHistoryPoint(BaseModel):
    period: str
    value: float
    date: dt.date | None = None


class MarketQuote(BaseModel):
    symbol: str
    name: str
    price: float
    change: float | None = None
    change_percent: float | None = None
    volume: int | None = None
    timestamp: dt.datetime
    provider: str
    data_status: str = "demo"
    source: str | None = "Demo Market Catalog"
    source_url: str | None = None
    sector: str | None = None
    retrieved_at: dt.datetime | None = None


class MarketIndexRecord(BaseModel):
    symbol: str
    name: str
    value: float
    change: float | None = None
    change_percent: float | None = None
    timestamp: dt.datetime
    provider: str
    data_status: str = "demo"
    source: str | None = "Demo Market Catalog"
    retrieved_at: dt.datetime | None = None


class NewsRecord(BaseModel):
    id: str | None = None
    headline: str
    summary: str
    source: str
    source_url: str | None = None
    published_at: dt.datetime
    category: str = "MARKET"
    related_entities: list[str] = Field(default_factory=list)
    related_sectors: list[str] = Field(default_factory=list)
    countries: list[str] = Field(default_factory=list)
    language: str = "en"
    author: str | None = None
    content_hash: str | None = None
    freshness: str = "CURRENT"
    age_hours: float | None = None
    provider: str = "demo"
    data_status: str = "demo"
    retrieved_at: dt.datetime | None = None

    def compute_hash(self) -> str:
        raw = f"{self.headline.strip().lower()}|{self.source.strip().lower()}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


class MacroRecord(BaseModel):
    indicator: str
    value: float
    unit: str
    period: str
    previous_value: float | None = None
    change: float | None = None
    source: str
    provider: str
    data_status: str = "demo"
    retrieved_at: dt.datetime | None = None


class GeopoliticalRecord(BaseModel):
    id: str | None = None
    title: str
    description: str | None = None
    region: str
    country: str
    category: str
    severity: int = 50
    event_date: dt.datetime
    market_relevance: int = 50
    related_sectors: list[str] = Field(default_factory=list)
    affected_assets: list[str] = Field(default_factory=list)
    freshness: str = "CURRENT"
    age_hours: float | None = None
    provider: str = "demo"
    data_status: str = "demo"
    source: str | None = "Demo Geopolitical Catalog"
    retrieved_at: dt.datetime | None = None


class AnnouncementRecord(BaseModel):
    id: str | None = None
    title: str
    category: str = "REGULATORY"
    announcement_type: str = "ANNOUNCEMENT"
    date: dt.date
    importance: str = "medium"
    source: str = "Demo Announcement Catalog"
    source_url: str | None = None
    related_sectors: list[str] = Field(default_factory=list)
    related_entities: list[str] = Field(default_factory=list)
    provider: str = "demo"
    data_status: str = "demo"
    retrieved_at: dt.datetime | None = None


class FetchResult(BaseModel):
    items: list[Any]
    source_state: SourceState
    data_status: str
    provider: str
