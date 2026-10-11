"""Geopolitical intelligence API routes."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.schemas.geopolitics import (
    GeopoliticalEventResponse,
    GeopoliticalListResponse,
    RegionsResponse,
)
from app.services.geopolitics import (
    get_geopolitical_event,
    get_regions_summary,
    list_geopolitical_events,
)

router = APIRouter(tags=["geopolitics"])


@router.get("", response_model=GeopoliticalListResponse)
def get_all_events(
    country: str = Query(default="", description="Country filter"),
    region: str = Query(default="", description="Region filter"),
    category: str = Query(default="", description="Category filter"),
    severity: str = Query(default="", description="Severity filter: LOW, MODERATE, HIGH, CRITICAL"),
    sector: str = Query(default="", description="Affected sector filter"),
) -> GeopoliticalListResponse:
    """Retrieve geopolitical intelligence events with filters."""
    return list_geopolitical_events(
        country=country,
        region=region,
        category=category,
        severity_level=severity,
        sector=sector,
    )


@router.get("/regions", response_model=RegionsResponse)
def get_regions() -> RegionsResponse:
    """Retrieve regional overview and average geopolitical risk severity."""
    return get_regions_summary()


@router.get("/country/{country}", response_model=GeopoliticalListResponse)
def get_events_by_country(country: str) -> GeopoliticalListResponse:
    """Retrieve geopolitical events impacting a specific country."""
    return list_geopolitical_events(country=country)


@router.get("/sector/{sector}", response_model=GeopoliticalListResponse)
def get_events_by_sector(sector: str) -> GeopoliticalListResponse:
    """Retrieve geopolitical events impacting a specific sector."""
    return list_geopolitical_events(sector=sector)


@router.get("/severity/{severity}", response_model=GeopoliticalListResponse)
def get_events_by_severity(severity: str) -> GeopoliticalListResponse:
    """Retrieve geopolitical events matching a specific severity tier."""
    return list_geopolitical_events(severity_level=severity)


@router.get("/{id}", response_model=GeopoliticalEventResponse)
def get_single_event(id: str) -> GeopoliticalEventResponse:
    """Retrieve a single geopolitical event by ID."""
    return get_geopolitical_event(id)
