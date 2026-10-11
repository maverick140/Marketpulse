"""End-to-end integration tests for dynamic stock search and selection."""

import os
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_dynamic_stock_search_and_selection_live() -> None:
    """Test live dynamic search against real providers when DATA_MODE=live."""
    with patch.dict(os.environ, {"DATA_MODE": "live"}):
        from app.core.config import get_settings
        from app.adapters.registry import get_registry
        get_settings.cache_clear()
        get_registry.cache_clear()

        # 1. Search for a stock outside initial list (e.g. BHEL)
        res = client.get("/api/markets/search?q=BHEL")
        assert res.status_code == 200
        data = res.json()
        assert data["count"] > 0
        assert any("BHEL" in item["symbol"] for item in data["results"])

        # 2. Select the found ticker (e.g. BHEL.BO or BHEL)
        top_symbol = data["results"][0]["symbol"]

        # 3. Load dynamic quote
        quote_res = client.get(f"/api/markets/quote/{top_symbol}")
        assert quote_res.status_code == 200
        quote_data = quote_res.json()
        assert quote_data["price"] > 0
        assert "BHEL" in quote_data["symbol"] or "BHEL" in quote_data["name"]

        # 4. Load dynamic history
        hist_res = client.get(f"/api/markets/history/{top_symbol}?timeframe=1M")
        assert hist_res.status_code == 200
        hist_data = hist_res.json()
        assert len(hist_data["points"]) > 0

        # Reset registry
        get_settings.cache_clear()
        get_registry.cache_clear()


def test_dynamic_search_queries_live_multi() -> None:
    """Verify live search for NVDA, Tata Motors, Infosys."""
    with patch.dict(os.environ, {"DATA_MODE": "live"}):
        from app.core.config import get_settings
        from app.adapters.registry import get_registry
        get_settings.cache_clear()
        get_registry.cache_clear()

        for q, expected in [("NVDA", "NVDA"), ("Tata Motors", "TMCV"), ("Infosys", "INFY")]:
            res = client.get(f"/api/markets/search?q={q}")
            assert res.status_code == 200
            data = res.json()
            assert data["count"] > 0
            assert any(expected in item["symbol"] for item in data["results"])

        get_settings.cache_clear()
        get_registry.cache_clear()


def test_dynamic_search_nonexistent_returns_empty_and_404_on_quote() -> None:
    # Search for nonexistent entity
    search_res = client.get("/api/markets/search?q=XYZ_INVALID_STOCK_NONEXISTENT_99999")
    assert search_res.status_code == 200
    search_data = search_res.json()
    assert search_data["count"] == 0
    assert len(search_data["results"]) == 0

    # Direct quote lookup on invalid entity returns 404
    quote_res = client.get("/api/markets/quote/XYZ_INVALID_STOCK_NONEXISTENT_99999")
    assert quote_res.status_code == 404
