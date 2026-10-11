"""Tests for GET /api/health."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_application_starts() -> None:
    assert app.title == "MarketPulse AI"


def test_health_returns_ok() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "MarketPulse AI"
