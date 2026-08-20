"""Tests for sentiment analysis API endpoints."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_market_sentiment() -> None:
    response = client.get("/api/sentiment")
    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data
    assert "overall_label" in data
    assert "distribution" in data
    assert "sectors" in data
    assert len(data["sectors"]) > 0


def test_get_symbol_sentiment() -> None:
    response = client.get("/api/sentiment/symbol/RELIANCE")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "RELIANCE"
    assert "overall_label" in data
    assert "average_score" in data


def test_get_sector_sentiment() -> None:
    response = client.get("/api/sentiment/sectors")
    assert response.status_code == 200
    data = response.json()
    assert "sectors" in data
    assert data["total_sectors"] > 0


def test_get_sentiment_trends() -> None:
    response = client.get("/api/sentiment/trends?timeframe=7D")
    assert response.status_code == 200
    data = response.json()
    assert "trends" in data
    assert len(data["trends"]) == 7


def test_analyze_custom_text_endpoint() -> None:
    response = client.post(
        "/api/sentiment/analyze",
        json={"text": "Outstanding quarterly expansion with record profit and dividend payout."},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "positive"
    assert data["score"] > 0.0
    assert data["confidence"] > 0.5
