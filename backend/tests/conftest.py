"""Pytest global configuration and fixtures."""

import os
import pytest
from app.core.config import get_settings
from app.adapters.registry import get_registry


@pytest.fixture(autouse=True)
def reset_demo_environment(monkeypatch):
    """Ensure test suite runs against deterministic demo baseline unless explicitly parameterized."""
    monkeypatch.setenv("DATA_MODE", "demo")
    monkeypatch.setenv("MARKET_PROVIDER", "demo")
    monkeypatch.setenv("NEWS_PROVIDER", "demo")
    monkeypatch.setenv("MACRO_PROVIDER", "demo")
    monkeypatch.setenv("GEOPOLITICAL_PROVIDER", "demo")
    monkeypatch.setenv("ANNOUNCEMENT_PROVIDER", "demo")
    get_settings.cache_clear()
    get_registry.cache_clear()
    yield
    get_settings.cache_clear()
    get_registry.cache_clear()
