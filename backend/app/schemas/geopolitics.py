"""Geopolitical intelligence API schemas."""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class GeopoliticalEventResponse(BaseModel):
    id: str | None = None
    title: str = Field(examples=["Hypothetical trade-policy discussion in South Asia"])
    description: str | None = None
    region: str = Field(examples=["South Asia"])
    country: str = Field(examples=["India"])
    category: str = Field(examples=["Trade"])
    severity: int = Field(examples=[45])
    severity_label: str = Field(examples=["MODERATE"])
    event_date: datetime
    market_relevance: int = Field(examples=[60])
    related_sectors: list[str] = Field(default_factory=list)
    affected_assets: list[str] = Field(default_factory=list)
    freshness: str = Field(default="CURRENT", examples=["CURRENT", "RECENT", "BACKGROUND", "STALE"])
    age_hours: float | None = Field(default=None, examples=[4.2])
    provider: str = Field(examples=["demo"])
    data_status: str = Field(examples=["demo"])
    source: str = Field(examples=["Demo Geopolitical Catalog"])
    retrieved_at: datetime | None = None


class GeopoliticalListResponse(BaseModel):
    events: list[GeopoliticalEventResponse]
    total: int
    data_status: str = Field(examples=["demo"])
    retrieved_at: datetime


class RegionSummary(BaseModel):
    region: str
    event_count: int
    average_severity: float
    countries: list[str]


class RegionsResponse(BaseModel):
    regions: list[RegionSummary]
    total_regions: int
