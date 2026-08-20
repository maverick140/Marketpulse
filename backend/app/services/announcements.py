"""Announcements service layer."""

from __future__ import annotations

from datetime import datetime, timezone
from fastapi import HTTPException, status

from app.adapters.demo.announcements import DemoAnnouncementProvider
from app.adapters.normalized import AnnouncementRecord
from app.adapters.registry import get_registry
from app.schemas.announcements import AnnouncementListResponse, AnnouncementResponse


def list_announcements(
    category: str = "",
    importance: str = "",
    symbol: str = "",
) -> AnnouncementListResponse:
    registry = get_registry()
    gateway = registry.gateway
    demo_provider = DemoAnnouncementProvider()

    ann_result = gateway.fetch(
        provider_name=registry.announcement_provider.name,
        retrieve=registry.announcement_provider.list_announcements,
        persist=lambda repo, items: repo.save_announcements(items),
        load_cache=lambda repo: repo.load_announcements(),
        fallback=demo_provider.list_announcements,
    )
    records: list[AnnouncementRecord] = ann_result.items

    filtered = records
    if category.strip():
        cat_lower = category.strip().lower()
        filtered = [r for r in filtered if r.category.lower() == cat_lower]

    if importance.strip():
        imp_lower = importance.strip().lower()
        filtered = [r for r in filtered if r.importance.lower() == imp_lower]

    if symbol.strip():
        sym_upper = symbol.strip().upper()
        filtered = [
            r for r in filtered
            if any(sym_upper in ent.upper() for ent in r.related_entities)
        ]

    announcements = [
        AnnouncementResponse(
            id=r.id or f"ann-{i+1:02d}",
            title=r.title,
            category=r.category,
            announcement_type=r.announcement_type,
            date=r.date,
            importance=r.importance,
            source=r.source,
            source_url=r.source_url,
            related_sectors=r.related_sectors,
            related_entities=r.related_entities,
            provider=r.provider,
            data_status=r.data_status,
            retrieved_at=r.retrieved_at,
        )
        for i, r in enumerate(filtered)
    ]

    return AnnouncementListResponse(
        announcements=announcements,
        total=len(announcements),
        data_status=ann_result.data_status,
        retrieved_at=datetime.now(timezone.utc),
    )


def get_announcement(announcement_id: str) -> AnnouncementResponse:
    list_resp = list_announcements()
    target = announcement_id.strip().lower()

    for item in list_resp.announcements:
        if item.id and item.id.lower() == target:
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Announcement '{announcement_id}' not found.",
    )
