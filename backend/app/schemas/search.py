"""Unified Global Search schemas."""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class SearchResultItem(BaseModel):
    category: str = Field(examples=["Markets", "Macro", "News", "Geopolitics", "Announcements"])
    title: str
    subtitle: str | None = None
    identifier: str
    data_status: str = "demo"
    relevance_score: float = 1.0


class UnifiedSearchResponse(BaseModel):
    query: str
    total_results: int
    markets: list[SearchResultItem]
    macro: list[SearchResultItem]
    news: list[SearchResultItem]
    geopolitics: list[SearchResultItem]
    announcements: list[SearchResultItem]
    generated_at: datetime
