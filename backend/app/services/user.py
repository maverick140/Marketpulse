"""User features, Watchlist, and Research workspace service layer.

Provides in-memory operation with opportunistic SQLite persistence. Never fails
if the database is missing or unwriteable.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models.market import Watchlist
from app.database.models.ops import SavedResearch
from app.schemas.user import (
    SavedResearchItem,
    SavedResearchListResponse,
    SavedResearchRequest,
    UserPreferences,
    WatchlistItem,
    WatchlistRequest,
    WatchlistResponse,
)

_PREFERENCES = UserPreferences(
    theme="dark",
    default_timeframe="1M",
    disclaimer_acknowledged=True,
    alert_notifications_enabled=True,
)

# In-memory store (used directly or as fallback)
_MEMORY_WATCHLIST: dict[str, WatchlistItem] = {
    "RELIANCE": WatchlistItem(symbol="RELIANCE", name="Reliance Industries Ltd", added_at=datetime.now(timezone.utc)),
    "INFY": WatchlistItem(symbol="INFY", name="Infosys Ltd", added_at=datetime.now(timezone.utc)),
    "TCS": WatchlistItem(symbol="TCS", name="Tata Consultancy Services Ltd", added_at=datetime.now(timezone.utc)),
}

_MEMORY_RESEARCH: dict[str, SavedResearchItem] = {
    "1": SavedResearchItem(
        id="1",
        title="Indian IT Export Resilience Study",
        query="Technology Sector & Export Demand Outlook",
        summary="Analysis on IT margin resilience amidst cross-border currency and inflation stability.",
        tags=["IT", "Macro", "Exports"],
        created_at=datetime.now(timezone.utc),
    )
}


def _init_user_seeds(session: Session) -> None:
    """Seed initial watchlist and research if empty in DB."""
    try:
        if session.query(Watchlist).count() == 0:
            session.add_all(
                [
                    Watchlist(symbol="RELIANCE", label="Reliance Industries Ltd"),
                    Watchlist(symbol="INFY", label="Infosys Ltd"),
                    Watchlist(symbol="TCS", label="Tata Consultancy Services Ltd"),
                ]
            )
            session.commit()
        if session.query(SavedResearch).count() == 0:
            session.add(
                SavedResearch(
                    id=1,
                    title="Indian IT Export Resilience Study",
                    content=json.dumps(
                        {
                            "query": "Technology Sector & Export Demand Outlook",
                            "summary": "Analysis on IT margin resilience amidst cross-border currency and inflation stability.",
                            "tags": ["IT", "Macro", "Exports"],
                        }
                    ),
                    export_format="json",
                )
            )
            session.commit()
    except Exception:
        session.rollback()


def get_watchlist() -> WatchlistResponse:
    try:
        session = SessionLocal()
        try:
            _init_user_seeds(session)
            rows = session.query(Watchlist).all()
            if rows:
                items = [
                    WatchlistItem(
                        symbol=r.symbol,
                        name=r.label or r.symbol,
                        added_at=r.created_at or datetime.now(timezone.utc),
                    )
                    for r in rows
                ]
                return WatchlistResponse(items=items, total=len(items))
        finally:
            session.close()
    except Exception:
        pass

    items = list(_MEMORY_WATCHLIST.values())
    return WatchlistResponse(items=items, total=len(items))


def add_to_watchlist(req: WatchlistRequest) -> WatchlistItem:
    sym = req.symbol.strip().upper()
    item = WatchlistItem(
        symbol=sym,
        name=f"{sym} (Tracked)",
        added_at=datetime.now(timezone.utc),
    )
    _MEMORY_WATCHLIST[sym] = item

    try:
        session = SessionLocal()
        try:
            existing = session.query(Watchlist).filter(Watchlist.symbol == sym).first()
            if not existing:
                item_db = Watchlist(symbol=sym, label=f"{sym} (Tracked)")
                session.add(item_db)
                session.commit()
        finally:
            session.close()
    except Exception:
        pass

    return item


def remove_from_watchlist(symbol: str) -> dict[str, str]:
    sym = symbol.strip().upper()
    found = False

    if sym in _MEMORY_WATCHLIST:
        del _MEMORY_WATCHLIST[sym]
        found = True

    try:
        session = SessionLocal()
        try:
            existing = session.query(Watchlist).filter(Watchlist.symbol == sym).first()
            if existing:
                session.delete(existing)
                session.commit()
                found = True
        finally:
            session.close()
    except Exception:
        pass

    if found:
        return {"status": "success", "message": f"{sym} removed from watchlist."}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Symbol '{symbol}' not in watchlist.",
    )


def list_saved_research() -> SavedResearchListResponse:
    try:
        session = SessionLocal()
        try:
            _init_user_seeds(session)
            rows = session.query(SavedResearch).all()
            if rows:
                items: list[SavedResearchItem] = []
                for r in rows:
                    tags = []
                    summary = r.content
                    query = r.title
                    try:
                        data = json.loads(r.content)
                        summary = data.get("summary", r.content)
                        query = data.get("query", r.title)
                        tags = data.get("tags", [])
                    except Exception:
                        pass
                    items.append(
                        SavedResearchItem(
                            id=str(r.id),
                            title=r.title,
                            query=query,
                            summary=summary,
                            tags=tags,
                            created_at=r.created_at or datetime.now(timezone.utc),
                        )
                    )
                return SavedResearchListResponse(items=items, total=len(items))
        finally:
            session.close()
    except Exception:
        pass

    items = list(_MEMORY_RESEARCH.values())
    return SavedResearchListResponse(items=items, total=len(items))


def save_research(req: SavedResearchRequest) -> SavedResearchItem:
    new_id = str(len(_MEMORY_RESEARCH) + 1)
    item = SavedResearchItem(
        id=new_id,
        title=req.title,
        query=req.query,
        summary=req.summary,
        tags=req.tags,
        created_at=datetime.now(timezone.utc),
    )
    _MEMORY_RESEARCH[new_id] = item

    try:
        session = SessionLocal()
        try:
            payload = json.dumps(
                {
                    "query": req.query,
                    "summary": req.summary,
                    "tags": req.tags,
                }
            )
            research_db = SavedResearch(
                title=req.title,
                content=payload,
                export_format="json",
            )
            session.add(research_db)
            session.commit()
            session.refresh(research_db)
            item.id = str(research_db.id)
            _MEMORY_RESEARCH[item.id] = item
        finally:
            session.close()
    except Exception:
        pass

    return item


def delete_saved_research(research_id: str) -> dict[str, str]:
    found = False
    if research_id in _MEMORY_RESEARCH:
        del _MEMORY_RESEARCH[research_id]
        found = True

    try:
        session = SessionLocal()
        try:
            target_id = int(research_id) if research_id.isdigit() else None
            if target_id:
                item = session.query(SavedResearch).filter(SavedResearch.id == target_id).first()
                if item:
                    session.delete(item)
                    session.commit()
                    found = True
        finally:
            session.close()
    except Exception:
        pass

    if found:
        return {"status": "success", "message": f"Research note '{research_id}' deleted."}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Research note '{research_id}' not found.",
    )


def get_user_preferences() -> UserPreferences:
    return _PREFERENCES


def update_user_preferences(prefs: UserPreferences) -> UserPreferences:
    global _PREFERENCES
    _PREFERENCES = prefs
    return _PREFERENCES
