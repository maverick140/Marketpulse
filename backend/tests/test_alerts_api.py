"""Tests for Alerts and Monitoring API routes."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_all_alerts() -> None:
    response = client.get("/api/alerts")
    assert response.status_code == 200
    data = response.json()
    assert "alerts" in data
    assert data["total"] >= 1
    first = data["alerts"][0]
    assert "id" in first
    assert "alert_type" in first
    assert "severity" in first
    assert "message" in first
    assert "explanation" in first
    assert first["severity"] in {"INFO", "WARNING", "CRITICAL"}


def test_filter_alerts_by_type() -> None:
    response = client.get("/api/alerts?type=GEOPOLITICAL_RISK")
    assert response.status_code == 200
    data = response.json()
    if data["total"] > 0:
        assert all(a["alert_type"] == "GEOPOLITICAL_RISK" for a in data["alerts"])


def test_filter_alerts_by_severity() -> None:
    response = client.get("/api/alerts?severity=WARNING")
    assert response.status_code == 200
    data = response.json()
    if data["total"] > 0:
        assert all(a["severity"] == "WARNING" for a in data["alerts"])


def test_get_single_alert_success() -> None:
    list_res = client.get("/api/alerts")
    first_id = list_res.json()["alerts"][0]["id"]

    response = client.get(f"/api/alerts/{first_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == first_id
    assert "message" in data


def test_get_single_alert_not_found() -> None:
    response = client.get("/api/alerts/nonexistent-alert-999")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
