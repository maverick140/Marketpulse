"""Tests for historical price generation and timeframe handling."""

from app.adapters.demo.catalog import generate_demo_history
from app.adapters.demo.market import DemoMarketProvider


def test_timeframe_candle_counts() -> None:
    provider = DemoMarketProvider()

    h_1d = provider.get_history("RELIANCE", "1D")
    assert len(h_1d) == 24

    h_5d = provider.get_history("RELIANCE", "5D")
    assert len(h_5d) == 30

    h_1m = provider.get_history("RELIANCE", "1M")
    assert len(h_1m) == 30

    h_3m = provider.get_history("RELIANCE", "3M")
    assert len(h_3m) == 45

    h_6m = provider.get_history("RELIANCE", "6M")
    assert len(h_6m) == 60

    h_1y = provider.get_history("RELIANCE", "1Y")
    assert len(h_1y) == 52


def test_history_candle_integrity() -> None:
    raw = generate_demo_history(2500.0, "1M")
    for candle in raw:
        assert candle["high"] >= candle["low"]
        assert candle["high"] >= min(candle["open"], candle["close"])
        assert candle["low"] <= max(candle["open"], candle["close"])
        assert candle["volume"] >= 0

    # Ensure chronological order
    for i in range(1, len(raw)):
        assert raw[i]["timestamp"] > raw[i - 1]["timestamp"]
