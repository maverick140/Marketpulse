"""Tests for announcements API routes."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_all_announcements() -> None:
    response = client.get("/api/announcements")
    assert response.status_code == 200
    data = response.json()
    assert "announcements" in data
    assert data["total"] >= 5
    first = data["announcements"][0]
    assert "title" in first
    assert "category" in first
    assert "announcement_type" in first
    assert "importance" in first
    assert first["data_status"] == "demo"


def test_filter_announcements_by_category() -> None:
    response = client.get("/api/announcements?category=COMPANY")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert all(a["category"] == "COMPANY" for a in data["announcements"])


def test_get_single_announcement_success() -> None:
    list_res = client.get("/api/announcements")
    first_id = list_res.json()["announcements"][0]["id"]

    response = client.get(f"/api/announcements/{first_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == first_id
    assert "title" in data


def test_get_single_announcement_not_found() -> None:
    response = client.get("/api/announcements/nonexistent-ann-999")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
