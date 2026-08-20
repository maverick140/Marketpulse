"""Tests for AI Intelligence API routes."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_ai_insights_endpoint() -> None:
    response = client.get("/api/ai/insights")
    assert response.status_code == 200
    data = response.json()
    assert "insights" in data
    assert data["total"] >= 3
    first = data["insights"][0]
    assert "summary" in first
    assert "market_context" in first
    assert "macro_factors" in first
    assert "evidence" in first
    assert "disclaimer" in first


def test_post_ai_research_endpoint() -> None:
    payload = {
        "query": "What are the key risk flags for energy commodities and regional supply chains?",
        "sector": "Energy",
    }
    response = client.post("/api/ai/research", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == payload["query"]
    assert "summary" in data
    assert "risk_factors" in data
    assert "uncertainties" in data
    assert len(data["evidence"]) >= 1


def test_distinct_queries_produce_distinct_research():
    res1 = client.post("/api/ai/research", json={"query": "What is happening with crude oil?"}).json()
    res2 = client.post("/api/ai/research", json={"query": "Explain the latest geopolitical risks affecting markets."}).json()
    res3 = client.post("/api/ai/research", json={"query": "What could cause the Indian rupee to weaken?"}).json()

    assert res1["summary"] != res2["summary"]
    assert res2["summary"] != res3["summary"]
    assert "oil" in res1["summary"].lower() or "crude" in res1["summary"].lower()
    assert "geopolitical" in res2["summary"].lower()
    assert "rupee" in res3["summary"].lower()
