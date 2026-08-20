"""GET /api/system/providers tests."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_system_providers_lists_demo_adapters() -> None:
    response = client.get("/api/system/providers")
    assert response.status_code == 200
    payload = response.json()
    providers = payload["providers"]
    types = {item["type"] for item in providers}
    assert types == {"market", "news", "macro", "geopolitical", "announcement"}
    assert all(item["provider"] == "demo" for item in providers)
    assert all(item["mode"] == "demo" for item in providers)
    assert all(item["status"] == "available" for item in providers)
    body = response.text.lower()
    for token in ("password", "secret", "api_key", "token"):
        assert token not in body
