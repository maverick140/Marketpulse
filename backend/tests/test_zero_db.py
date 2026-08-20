"""Verify that MarketPulse AI operates 100% without a database."""

from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def failing_session_local():
    raise RuntimeError("Database completely unavailable / No PostgreSQL / No SQLite")


def test_market_quote_without_database():
    with patch("app.adapters.gateway.SessionLocal", side_effect=failing_session_local):
        res = client.get("/api/markets/quote/RELIANCE")
        assert res.status_code == 200
        data = res.json()
        assert data["symbol"] == "RELIANCE"
        assert data["price"] > 0


def test_market_history_and_indicators_without_database():
    with patch("app.adapters.gateway.SessionLocal", side_effect=failing_session_local):
        hist_res = client.get("/api/markets/history/RELIANCE?timeframe=1M")
        assert hist_res.status_code == 200
        assert len(hist_res.json()["points"]) > 0

        ind_res = client.get("/api/markets/indicators/RELIANCE?timeframe=1M")
        assert ind_res.status_code == 200
        assert ind_res.json()["symbol"] == "RELIANCE"


def test_macro_and_news_without_database():
    with patch("app.adapters.gateway.SessionLocal", side_effect=failing_session_local):
        macro_res = client.get("/api/macro")
        assert macro_res.status_code == 200
        assert macro_res.json()["count"] >= 4

        news_res = client.get("/api/news")
        assert news_res.status_code == 200
        assert news_res.json()["total"] >= 1


def test_geopolitics_risk_ai_without_database():
    with patch("app.adapters.gateway.SessionLocal", side_effect=failing_session_local):
        geo_res = client.get("/api/geopolitics")
        assert geo_res.status_code == 200
        assert geo_res.json()["total"] >= 1

        risk_res = client.get("/api/risk/overview")
        assert risk_res.status_code == 200
        assert "market_risk_score" in risk_res.json()

        ai_res = client.get("/api/ai/insights")
        assert ai_res.status_code == 200
        assert ai_res.json()["total"] >= 1


def test_user_watchlist_without_database():
    with patch("app.services.user.SessionLocal", side_effect=failing_session_local):
        wl_res = client.get("/api/user/watchlist")
        assert wl_res.status_code == 200
        assert wl_res.json()["total"] >= 1

        add_res = client.post("/api/user/watchlist", json={"symbol": "TATAMOTORS"})
        assert add_res.status_code == 200
        assert add_res.json()["symbol"] == "TATAMOTORS"
