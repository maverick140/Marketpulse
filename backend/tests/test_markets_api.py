"""Tests for market data API endpoints."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_market_overview() -> None:
    response = client.get("/api/markets/overview")
    assert response.status_code == 200
    data = response.json()
    assert "indices" in data
    assert "gainers" in data
    assert "decliners" in data
    assert "most_active" in data
    assert len(data["indices"]) >= 4
    assert len(data["gainers"]) > 0
    assert len(data["decliners"]) > 0
    assert len(data["most_active"]) > 0
    assert data["data_status"] in {"demo", "cached", "live"}


def test_search_securities() -> None:
    # Search by ticker symbol
    response = client.get("/api/markets/search?q=INFY")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 1
    assert any(item["symbol"] == "INFY" for item in data["results"])

    # Search by sector
    response = client.get("/api/markets/search?q=Energy")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 1
    assert any(item["symbol"] == "RELIANCE" for item in data["results"])


def test_get_quote_success() -> None:
    response = client.get("/api/markets/quote/RELIANCE")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "RELIANCE"
    assert data["price"] > 0
    assert data["data_status"] in {"demo", "cached", "live"}
    assert data["provider"] in {"demo", "free"}


def test_get_quote_not_found() -> None:
    response = client.get("/api/markets/quote/UNKNOWN_XYZ_99999_NONEXISTENT")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert "not found" in data["error"]["message"].lower()


def test_search_nonexistent_stock_empty_results() -> None:
    response = client.get("/api/markets/search?q=XYZ_INVALID_STOCK_123456789")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert len(data["results"]) == 0


def test_get_history_success() -> None:
    response = client.get("/api/markets/history/TCS?timeframe=1M")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "TCS"
    assert data["timeframe"] == "1M"
    assert len(data["points"]) == 30
    first_pt = data["points"][0]
    assert "open" in first_pt
    assert "high" in first_pt
    assert "low" in first_pt
    assert "close" in first_pt
    assert "volume" in first_pt


def test_get_history_invalid_timeframe() -> None:
    response = client.get("/api/markets/history/TCS?timeframe=10Y")
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "invalid timeframe" in data["error"]["message"].lower()


def test_get_indicators_success() -> None:
    response = client.get("/api/markets/indicators/INFY?timeframe=1M")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "INFY"
    assert data["timeframe"] == "1M"
    assert "sma_20" in data
    assert "rsi_14" in data
    assert "macd" in data
    assert "volatility" in data
    assert "max_drawdown" in data
    assert "period_return" in data
    assert "disclaimer" in data
    assert "Educational demonstration only" in data["disclaimer"]
