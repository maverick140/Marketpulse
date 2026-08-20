"""Tests for geopolitical intelligence API routes."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_all_geopolitical_events() -> None:
    response = client.get("/api/geopolitics")
    assert response.status_code == 200
    data = response.json()
    assert "events" in data
    assert data["total"] >= 5
    first = data["events"][0]
    assert "title" in first
    assert "region" in first
    assert "country" in first
    assert "severity" in first
    assert "severity_label" in first
    assert first["severity_label"] in {"LOW", "MODERATE", "HIGH", "CRITICAL"}
    assert first["data_status"] == "demo"


def test_get_regions_summary() -> None:
    response = client.get("/api/geopolitics/regions")
    assert response.status_code == 200
    data = response.json()
    assert "regions" in data
    assert data["total_regions"] >= 3
    first = data["regions"][0]
    assert "region" in first
    assert "event_count" in first
    assert "average_severity" in first


def test_filter_events_by_country() -> None:
    response = client.get("/api/geopolitics/country/India")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert all(e["country"].lower() == "india" for e in data["events"])


def test_filter_events_by_sector() -> None:
    response = client.get("/api/geopolitics/sector/Energy")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any("Energy" in e["related_sectors"] for e in data["events"])


def test_filter_events_by_severity() -> None:
    response = client.get("/api/geopolitics/severity/HIGH")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert all(e["severity_label"] == "HIGH" for e in data["events"])


def test_get_single_event_success() -> None:
    list_res = client.get("/api/geopolitics")
    first_id = list_res.json()["events"][0]["id"]

    response = client.get(f"/api/geopolitics/{first_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == first_id
    assert "title" in data


def test_get_single_event_not_found() -> None:
    response = client.get("/api/geopolitics/nonexistent-geo-999")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
