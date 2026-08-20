"""Tests for GET /api/system/status."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_system_status_success() -> None:
    response = client.get("/api/system/status")
    assert response.status_code == 200
    payload = response.json()
    assert payload["application_status"] == "online"
    assert payload["environment"]
    assert payload["data_mode"]
    assert payload["database_status"] == "online"
    assert payload["api_version"]
    assert set(payload.keys()) == {
        "application_status",
        "environment",
        "data_mode",
        "database_status",
        "api_version",
    }


def test_system_status_does_not_expose_secrets() -> None:
    response = client.get("/api/system/status")
    body = response.text.lower()
    for token in ("password", "secret", "api_key", "token"):
        assert token not in body
