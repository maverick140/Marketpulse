"""Tests for Risk and Scenario Lab API routes."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_risk_overview() -> None:
    response = client.get("/api/risk/overview")
    assert response.status_code == 200
    data = response.json()
    assert "market_risk_score" in data
    assert 0 <= data["market_risk_score"] <= 100
    assert "risk_tier" in data
    assert "market_regime" in data
    assert "volatility_index" in data
    assert "top_drivers" in data
    assert "sector_risks" in data


def test_get_security_risk() -> None:
    response = client.get("/api/risk/symbol/INFY")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "INFY"
    assert "risk_score" in data
    assert "beta" in data
    assert "volatility" in data
    assert "max_drawdown" in data
    assert "volume_anomaly_ratio" in data


def test_post_scenario_simulation() -> None:
    payload = {"scenario_type": "Crude Oil Surge", "magnitude": 25.0}
    response = client.post("/api/risk/scenario", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["scenario_type"] == payload["scenario_type"]
    assert "estimated_market_impact_percent" in data
    assert "simulated_market_price" in data
    assert "sector_impacts" in data
    assert "disclaimer" in data


def test_get_correlation_matrix() -> None:
    response = client.get("/api/risk/correlation")
    assert response.status_code == 200
    data = response.json()
    assert "assets" in data
    assert "matrix" in data
    assert len(data["assets"]) == len(data["matrix"])
    assert data["matrix"][0][0] == 1.0
