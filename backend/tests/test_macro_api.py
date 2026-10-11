"""Tests for macroeconomic data API endpoints with official Excel dataset integration."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings
from app.adapters.registry import get_registry

client = TestClient(app)


@pytest.fixture(autouse=True)
def live_macro_environment(monkeypatch):
    """Run macro API tests against live/free provider with raw/ Excel integration."""
    monkeypatch.setenv("DATA_MODE", "live")
    monkeypatch.setenv("MACRO_PROVIDER", "free")
    get_settings.cache_clear()
    get_registry.cache_clear()
    yield
    get_settings.cache_clear()
    get_registry.cache_clear()


def test_list_macro_indicators() -> None:
    response = client.get("/api/macro")
    assert response.status_code == 200
    data = response.json()
    assert "indicators" in data
    assert data["count"] >= 3
    names = {ind["indicator"] for ind in data["indicators"]}

    # Must contain the three official indicators from raw/ Excel workbooks
    assert "Real GDP Growth" in names
    assert "CPI Inflation" in names
    assert "Policy Repo Rate" in names

    # Unemployment must be completely absent
    assert not any("unemployment" in n.lower() for n in names)

    # Official indicators must have data_status "official"
    gdp = next(ind for ind in data["indicators"] if ind["indicator"] == "Real GDP Growth")
    assert gdp["value"] == 7.80
    assert gdp["unit"] == "%"
    assert "2026-27 Q1" in gdp["period"]
    assert gdp["data_status"] == "official"

    cpi = next(ind for ind in data["indicators"] if ind["indicator"] == "CPI Inflation")
    assert cpi["value"] == 4.82
    assert cpi["unit"] == "%"
    assert "August 2026" in cpi["period"]
    assert cpi["data_status"] == "official"

    repo = next(ind for ind in data["indicators"] if ind["indicator"] == "Policy Repo Rate")
    assert repo["value"] == 5.50
    assert repo["unit"] == "%"
    assert "2026" in repo["period"]
    assert repo["data_status"] == "official"


def test_get_macro_detail_gdp_success() -> None:
    response = client.get("/api/macro/Real%20GDP%20Growth")
    assert response.status_code == 200
    data = response.json()
    assert data["indicator"] == "Real GDP Growth"
    assert data["current"]["value"] == 7.80
    assert len(data["history"]) == 13
    assert data["history"][0]["period"] == "2023-24 Q1"
    assert data["history"][-1]["period"] == "2026-27 Q1"


def test_get_macro_detail_alias_gdp_success() -> None:
    response = client.get("/api/macro/GDP%20Growth")
    assert response.status_code == 200
    data = response.json()
    assert data["indicator"] == "Real GDP Growth"
    assert data["current"]["value"] == 7.80


def test_get_macro_detail_cpi_success() -> None:
    response = client.get("/api/macro/CPI%20Inflation")
    assert response.status_code == 200
    data = response.json()
    assert data["indicator"] == "CPI Inflation"
    assert data["current"]["value"] == 4.82
    assert len(data["history"]) == 8
    assert data["history"][0]["period"] == "Jan 2026"
    assert data["history"][-1]["period"] == "Aug 2026"


def test_get_macro_detail_repo_success() -> None:
    response = client.get("/api/macro/Policy%20Repo%20Rate")
    assert response.status_code == 200
    data = response.json()
    assert data["indicator"] == "Policy Repo Rate"
    assert data["current"]["value"] == 5.50
    assert len(data["history"]) >= 50
    assert data["history"][-1]["value"] == 5.50


def test_get_macro_detail_not_found() -> None:
    response = client.get("/api/macro/nonexistent_indicator")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert "not found" in data["error"]["message"].lower()
