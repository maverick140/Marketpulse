"""Tests for User Watchlist, Saved Research, and Preferences API."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_watchlist_crud_flow() -> None:
    # 1. List watchlist
    list_res = client.get("/api/user/watchlist")
    assert list_res.status_code == 200
    assert list_res.json()["total"] >= 1

    # 2. Add item
    add_res = client.post("/api/user/watchlist", json={"symbol": "SBIN"})
    assert add_res.status_code == 200
    assert add_res.json()["symbol"] == "SBIN"

    # 3. Verify added
    list_after = client.get("/api/user/watchlist")
    symbols = [item["symbol"] for item in list_after.json()["items"]]
    assert "SBIN" in symbols

    # 4. Remove item
    del_res = client.delete("/api/user/watchlist/SBIN")
    assert del_res.status_code == 200


def test_saved_research_crud_flow() -> None:
    # 1. List saved research
    list_res = client.get("/api/user/research")
    assert list_res.status_code == 200
    assert list_res.json()["total"] >= 1

    # 2. Save new research
    payload = {
        "title": "Energy Commodities & Logistics Stress Note",
        "query": "Energy & Geopolitical Supply Chain Scenario",
        "summary": "Simulated oil shock and maritime route impact summary.",
        "tags": ["Energy", "Geopolitics", "Stress"],
    }
    save_res = client.post("/api/user/research", json=payload)
    assert save_res.status_code == 200
    created_id = save_res.json()["id"]

    # 3. Delete research
    del_res = client.delete(f"/api/user/research/{created_id}")
    assert del_res.status_code == 200


def test_preferences_get_and_update() -> None:
    get_res = client.get("/api/user/preferences")
    assert get_res.status_code == 200
    prefs = get_res.json()
    assert prefs["theme"] == "dark"

    updated = client.put(
        "/api/user/preferences",
        json={
            "theme": "dark",
            "default_timeframe": "3M",
            "disclaimer_acknowledged": True,
            "alert_notifications_enabled": True,
        },
    )
    assert updated.status_code == 200
    assert updated.json()["default_timeframe"] == "3M"
