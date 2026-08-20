"""User features, Watchlist, and Research workspace API routes."""

from __future__ import annotations

from fastapi import APIRouter

from app.schemas.user import (
    SavedResearchItem,
    SavedResearchListResponse,
    SavedResearchRequest,
    UserPreferences,
    WatchlistItem,
    WatchlistRequest,
    WatchlistResponse,
)
from app.services.user import (
    add_to_watchlist,
    delete_saved_research,
    get_user_preferences,
    get_watchlist,
    list_saved_research,
    remove_from_watchlist,
    save_research,
    update_user_preferences,
)

router = APIRouter(tags=["user"])


@router.get("/watchlist", response_model=WatchlistResponse)
def list_watchlist_endpoint() -> WatchlistResponse:
    """Retrieve user watchlist securities."""
    return get_watchlist()


@router.post("/watchlist", response_model=WatchlistItem)
def add_watchlist_endpoint(payload: WatchlistRequest) -> WatchlistItem:
    """Add a security to the user watchlist."""
    return add_to_watchlist(payload)


@router.delete("/watchlist/{symbol}")
def delete_watchlist_endpoint(symbol: str) -> dict[str, str]:
    """Remove a security from the user watchlist."""
    return remove_from_watchlist(symbol)


@router.get("/research", response_model=SavedResearchListResponse)
def list_research_endpoint() -> SavedResearchListResponse:
    """Retrieve saved research notes."""
    return list_saved_research()


@router.post("/research", response_model=SavedResearchItem)
def save_research_endpoint(payload: SavedResearchRequest) -> SavedResearchItem:
    """Save a research analysis to the user workspace."""
    return save_research(payload)


@router.delete("/research/{id}")
def delete_research_endpoint(id: str) -> dict[str, str]:
    """Delete a saved research note."""
    return delete_saved_research(id)


@router.get("/preferences", response_model=UserPreferences)
def get_preferences_endpoint() -> UserPreferences:
    """Retrieve user UI and notification preferences."""
    return get_user_preferences()


@router.put("/preferences", response_model=UserPreferences)
def update_preferences_endpoint(payload: UserPreferences) -> UserPreferences:
    """Update user UI and notification preferences."""
    return update_user_preferences(payload)
