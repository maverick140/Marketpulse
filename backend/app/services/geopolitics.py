"""Geopolitical intelligence service layer."""

from __future__ import annotations

from datetime import datetime, timezone
from fastapi import HTTPException, status

from app.adapters.demo.geopolitical import DemoGeopoliticalProvider
from app.adapters.normalized import GeopoliticalRecord
from app.adapters.registry import get_registry
from app.schemas.geopolitics import (
    GeopoliticalEventResponse,
    GeopoliticalListResponse,
    RegionSummary,
    RegionsResponse,
)


def get_severity_label(severity: int) -> str:
    if severity >= 75:
        return "CRITICAL"
    if severity >= 50:
        return "HIGH"
    if severity >= 25:
        return "MODERATE"
    return "LOW"


def list_geopolitical_events(
    country: str = "",
    region: str = "",
    category: str = "",
    severity_level: str = "",
    sector: str = "",
) -> GeopoliticalListResponse:
    registry = get_registry()
    gateway = registry.gateway
    demo_provider = DemoGeopoliticalProvider()

    geo_result = gateway.fetch(
        provider_name=registry.geopolitical_provider.name,
        retrieve=registry.geopolitical_provider.list_events,
        persist=lambda repo, items: repo.save_events(items),
        load_cache=lambda repo: repo.load_events(),
        fallback=demo_provider.list_events,
    )
    records: list[GeopoliticalRecord] = geo_result.items
    now = datetime.now(timezone.utc)

    # Sort strictly newest first
    records = sorted(records, key=lambda r: r.event_date, reverse=True)

    filtered = records

    if country.strip():
        c_lower = country.strip().lower()
        filtered = [r for r in filtered if r.country.lower() == c_lower]

    if region.strip():
        r_lower = region.strip().lower()
        filtered = [r for r in filtered if r.region.lower() == r_lower]

    if category.strip():
        cat_lower = category.strip().lower()
        filtered = [r for r in filtered if r.category.lower() == cat_lower]

    if severity_level.strip():
        sev_upper = severity_level.strip().upper()
        filtered = [r for r in filtered if get_severity_label(r.severity) == sev_upper]

    if sector.strip():
        sec_lower = sector.strip().lower()
        filtered = [
            r for r in filtered
            if any(sec_lower in s.lower() for s in r.related_sectors)
        ]

    events = []
    for i, r in enumerate(filtered):
        # Calculate dynamic age
        diff_s = max(0.0, (now - (r.event_date if r.event_date.tzinfo else r.event_date.replace(tzinfo=timezone.utc))).total_seconds())
        age_h = round(diff_s / 3600.0, 1)
        f_state = "CURRENT" if age_h <= 48.0 else ("RECENT" if age_h <= 120.0 else ("BACKGROUND" if age_h <= 336.0 else "STALE"))

        events.append(
            GeopoliticalEventResponse(
                id=r.id or f"geo-{i+1:02d}",
                title=r.title,
                description=r.description,
                region=r.region,
                country=r.country,
                category=r.category,
                severity=r.severity,
                severity_label=get_severity_label(r.severity),
                event_date=r.event_date,
                market_relevance=r.market_relevance,
                related_sectors=r.related_sectors,
                affected_assets=r.affected_assets,
                freshness=f_state,
                age_hours=age_h,
                provider=r.provider,
                data_status=r.data_status,
                source=r.source or "Demo Geopolitical Catalog",
                retrieved_at=r.retrieved_at or now,
            )
        )

    return GeopoliticalListResponse(
        events=events,
        total=len(events),
        data_status=geo_result.data_status,
        retrieved_at=now,
    )


def get_geopolitical_event(event_id: str) -> GeopoliticalEventResponse:
    list_resp = list_geopolitical_events()
    target = event_id.strip().lower()

    for e in list_resp.events:
        if e.id and e.id.lower() == target:
            return e

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Geopolitical event '{event_id}' not found.",
    )


def get_regions_summary() -> RegionsResponse:
    list_resp = list_geopolitical_events()
    reg_map: dict[str, list[GeopoliticalEventResponse]] = {}

    for e in list_resp.events:
        if e.region not in reg_map:
            reg_map[e.region] = []
        reg_map[e.region].append(e)

    summaries: list[RegionSummary] = []
    for reg, evs in reg_map.items():
        avg_sev = round(sum(ev.severity for ev in evs) / len(evs), 1)
        countries = sorted(list({ev.country for ev in evs}))
        summaries.append(
            RegionSummary(
                region=reg,
                event_count=len(evs),
                average_severity=avg_sev,
                countries=countries,
            )
        )

    return RegionsResponse(
        regions=summaries,
        total_regions=len(summaries),
    )
