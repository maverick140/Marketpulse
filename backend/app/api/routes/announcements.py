"""Announcements API routes."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.schemas.announcements import AnnouncementListResponse, AnnouncementResponse
from app.services.announcements import get_announcement, list_announcements

router = APIRouter(tags=["announcements"])


@router.get("", response_model=AnnouncementListResponse)
def get_all_announcements(
    category: str = Query(default="", description="Category filter"),
    importance: str = Query(default="", description="Importance level filter (high, medium, low)"),
    symbol: str = Query(default="", description="Associated symbol filter"),
) -> AnnouncementListResponse:
    """Retrieve corporate, regulatory, and policy announcements."""
    return list_announcements(category=category, importance=importance, symbol=symbol)


@router.get("/{id}", response_model=AnnouncementResponse)
def get_single_announcement(id: str) -> AnnouncementResponse:
    """Retrieve a single announcement by ID."""
    return get_announcement(id)
