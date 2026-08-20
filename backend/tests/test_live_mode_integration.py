"""Integration tests for live mode endpoints."""

from fastapi.testclient import TestClient
from app.core.config import get_settings
from app.adapters.registry import get_registry
from app.main import app

client = TestClient(app)


def test_live_mode_endpoints(monkeypatch):
    monkeypatch.setenv("DATA_MODE", "live")
    get_settings.cache_clear()
    get_registry.cache_clear()

    # 1. Market Quote
    res = client.get("/api/markets/quote/RELIANCE")
    assert res.status_code == 200
    data = res.json()
    assert data["symbol"] == "RELIANCE"
    assert data["price"] > 0
    assert data["data_status"] == "live"

    # 2. Market History
    res = client.get("/api/markets/history/RELIANCE?timeframe=1M")
    assert res.status_code == 200
    assert len(res.json()["points"]) > 0

    # 3. Macro
    res = client.get("/api/macro")
    assert res.status_code == 200
    assert res.json()["count"] >= 4
    assert res.json()["data_status"] == "live"

    # 4. News
    res = client.get("/api/news")
    assert res.status_code == 200
    assert res.json()["total"] >= 1
    assert res.json()["data_status"] == "live"

    # 5. Geopolitics
    res = client.get("/api/geopolitics")
    assert res.status_code == 200
    assert res.json()["total"] >= 1
    assert res.json()["data_status"] == "live"

    # 6. Geopolitics Regions
    res = client.get("/api/geopolitics/regions")
    assert res.status_code == 200
    assert res.json()["total_regions"] >= 1

    # 7. Announcements
    res = client.get("/api/announcements")
    assert res.status_code == 200
    assert res.json()["total"] >= 1
    assert res.json()["data_status"] == "live"

    # 8. Risk Overview
    res = client.get("/api/risk/overview")
    assert res.status_code == 200
    assert "market_risk_score" in res.json()

    # 9. AI Insights
    res = client.get("/api/ai/insights")
    assert res.status_code == 200
    assert res.json()["total"] >= 1

    # 10. System Status
    res = client.get("/api/system/status")
    assert res.status_code == 200
    assert res.json()["data_mode"] == "live"
