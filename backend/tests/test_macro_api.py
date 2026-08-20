"""Tests for macroeconomic data API endpoints."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_macro_indicators() -> None:
    response = client.get("/api/macro")
    assert response.status_code == 200
    data = response.json()
    assert "indicators" in data
    assert data["count"] >= 7
    names = {ind["indicator"] for ind in data["indicators"]}
    assert names >= {
        "Inflation",
        "Interest Rate",
        "GDP Growth",
        "Unemployment",
        "Oil",
        "Gold",
        "Currency",
    }
    assert all(ind["data_status"] == "demo" for ind in data["indicators"])


def test_get_macro_detail_success() -> None:
    response = client.get("/api/macro/Inflation")
    assert response.status_code == 200
    data = response.json()
    assert data["indicator"] == "Inflation"
    assert data["current"]["indicator"] == "Inflation"
    assert data["current"]["value"] == 4.8
    assert len(data["history"]) >= 4
    for h in data["history"]:
        assert "period" in h
        assert "value" in h


def test_get_macro_detail_not_found() -> None:
    response = client.get("/api/macro/nonexistent_indicator")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert "not found" in data["error"]["message"].lower()
