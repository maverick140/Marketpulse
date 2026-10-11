"""User features, Watchlist, and Research workspace schemas."""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class WatchlistItem(BaseModel):
    symbol: str
    name: str | None = None
    added_at: datetime


class WatchlistRequest(BaseModel):
    symbol: str


class WatchlistResponse(BaseModel):
    items: list[WatchlistItem]
    total: int


class SavedResearchItem(BaseModel):
    id: str
    title: str
    query: str
    summary: str
    tags: list[str] = Field(default_factory=list)
    created_at: datetime


class SavedResearchRequest(BaseModel):
    title: str
    query: str
    summary: str
    tags: list[str] = Field(default_factory=list)


class SavedResearchListResponse(BaseModel):
    items: list[SavedResearchItem]
    total: int


class UserPreferences(BaseModel):
    theme: str = "dark"
    default_timeframe: str = "1M"
    disclaimer_acknowledged: bool = True
    alert_notifications_enabled: bool = True
