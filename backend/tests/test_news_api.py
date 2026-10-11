"""Tests for news intelligence API routes and filtering."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_all_news() -> None:
    response = client.get("/api/news")
    assert response.status_code == 200
    data = response.json()
    assert "articles" in data
    assert data["total"] >= 5
    assert len(data["articles"]) >= 5
    first = data["articles"][0]
    assert "headline" in first
    assert "summary" in first
    assert "source" in first
    assert "category" in first
    assert first["data_status"] == "demo"


def test_news_search() -> None:
    response = client.get("/api/news/search?q=technology")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any("technology" in a["headline"].lower() or "technology" in a["category"].lower() for a in data["articles"])


def test_news_by_symbol() -> None:
    response = client.get("/api/news/symbol/RELIANCE")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any("RELIANCE" in a["related_entities"] for a in data["articles"])


def test_news_by_category() -> None:
    response = client.get("/api/news/category/COMMODITIES")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert all(a["category"] == "COMMODITIES" for a in data["articles"])


def test_news_by_country() -> None:
    response = client.get("/api/news/country/India")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


def test_get_single_news_success() -> None:
    list_res = client.get("/api/news")
    first_id = list_res.json()["articles"][0]["id"]

    response = client.get(f"/api/news/{first_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == first_id
    assert "headline" in data


def test_get_single_news_not_found() -> None:
    response = client.get("/api/news/nonexistent-id-999")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
