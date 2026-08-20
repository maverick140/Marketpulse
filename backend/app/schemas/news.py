"""News intelligence API schemas."""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class NewsArticleResponse(BaseModel):
    id: str | None = None
    headline: str = Field(examples=["Technology sector attention rises in educational sample"])
    summary: str = Field(examples=["Synthetic research note describing software-services trends."])
    source: str = Field(examples=["Demo Research Feed"])
    source_url: str | None = None
    published_at: datetime
    category: str = Field(examples=["TECHNOLOGY"])
    related_entities: list[str] = Field(default_factory=list)
    related_sectors: list[str] = Field(default_factory=list)
    countries: list[str] = Field(default_factory=list)
    language: str = Field(default="en")
    author: str | None = None
    freshness: str = Field(default="CURRENT", examples=["CURRENT", "RECENT", "BACKGROUND", "STALE"])
    age_hours: float | None = Field(default=None, examples=[3.5])
    provider: str = Field(examples=["demo"])
    data_status: str = Field(examples=["demo"])
    content_hash: str | None = None
    retrieved_at: datetime | None = None


class NewsListResponse(BaseModel):
    articles: list[NewsArticleResponse]
    total: int
    page: int
    page_size: int
    data_status: str = Field(examples=["demo"])
    retrieved_at: datetime
