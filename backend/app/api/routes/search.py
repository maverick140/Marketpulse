"""Unified Global Search API routes."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.schemas.search import UnifiedSearchResponse
from app.services.search import perform_unified_search

router = APIRouter(tags=["search"])


@router.get("", response_model=UnifiedSearchResponse)
def search_all(
    q: str = Query(default="", description="Search query string across all intelligence categories"),
) -> UnifiedSearchResponse:
    """Search across stocks, indices, macro indicators, news, geopolitics, and announcements."""
    return perform_unified_search(q)
