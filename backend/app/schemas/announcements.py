"""Announcements API schemas."""

from __future__ import annotations

import datetime as dt
from pydantic import BaseModel, Field


class AnnouncementResponse(BaseModel):
    id: str | None = None
    title: str = Field(examples=["Sample corporate results briefing"])
    category: str = Field(examples=["COMPANY"])
    announcement_type: str = Field(examples=["ANNOUNCEMENT"])
    date: dt.date
    importance: str = Field(examples=["high"])
    source: str = Field(examples=["Demo Announcement Catalog"])
    source_url: str | None = None
    related_sectors: list[str] = Field(default_factory=list)
    related_entities: list[str] = Field(default_factory=list)
    provider: str = Field(examples=["demo"])
    data_status: str = Field(examples=["demo"])
    retrieved_at: dt.datetime | None = None


class AnnouncementListResponse(BaseModel):
    announcements: list[AnnouncementResponse]
    total: int
    data_status: str = Field(examples=["demo"])
    retrieved_at: dt.datetime
