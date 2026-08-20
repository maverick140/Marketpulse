"""Security and error leakage validation tests."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_no_stack_trace_on_404() -> None:
    response = client.get("/api/nonexistent/endpoint/path")
    assert response.status_code == 404
    data = response.json()
    assert ("error" in data) or ("detail" in data)
    assert "traceback" not in data
    assert "Traceback" not in response.text


def test_no_stack_trace_on_422_validation_error() -> None:
    response = client.post("/api/sentiment/analyze", json={"invalid_field": 123})
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "validation_error"
    assert "traceback" not in data


def test_system_status_secrets_redaction() -> None:
    response = client.get("/api/system/status")
    assert response.status_code == 200
    data = response.json()
    text = response.text.lower()
    assert "password" not in text
    assert "secret" not in text
    assert "api_key" not in text


def test_cors_preflight_headers_present() -> None:
    response = client.options(
        "/api/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
