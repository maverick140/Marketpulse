"""Tests for Unified Global Search API routes."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_unified_search_across_domains() -> None:
    response = client.get("/api/search?q=technology")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "technology"
    assert data["total_results"] > 0
    assert "markets" in data
    assert "macro" in data
    assert "news" in data
    assert "geopolitics" in data
    assert "announcements" in data


def test_unified_search_empty_query() -> None:
    response = client.get("/api/search?q=")
    assert response.status_code == 200
    data = response.json()
    assert data["total_results"] == 0
