"""Tests for technical indicator calculations."""

from app.analytics.technical import (
    calculate_ema,
    calculate_macd,
    calculate_max_drawdown,
    calculate_returns,
    calculate_rsi,
    calculate_sma,
    calculate_volatility,
    compute_technical_indicators,
)


def test_calculate_sma() -> None:
    prices = [10.0, 20.0, 30.0, 40.0, 50.0]
    assert calculate_sma(prices, 3) == 40.0  # (30 + 40 + 50) / 3
    assert calculate_sma(prices, 10) is None


def test_calculate_ema() -> None:
    prices = [10.0, 20.0, 30.0, 40.0, 50.0]
    ema = calculate_ema(prices, 3)
    assert ema is not None
    assert ema > 0


def test_calculate_rsi() -> None:
    # Monotonically increasing prices should have RSI 100
    increasing = [float(i) for i in range(1, 20)]
    assert calculate_rsi(increasing, 14) == 100.0

    # Constant prices
    constant = [100.0] * 20
    assert calculate_rsi(constant, 14) is not None

    # Insufficient data
    assert calculate_rsi([10.0, 12.0], 14) is None


def test_calculate_macd() -> None:
    prices = [float(100 + i * 2) for i in range(40)]
    macd = calculate_macd(prices, 12, 26, 9)
    assert macd["macd_line"] is not None
    assert macd["signal_line"] is not None
    assert macd["histogram"] is not None


def test_calculate_volatility() -> None:
    prices = [100.0, 105.0, 95.0, 102.0, 98.0, 104.0]
    vol = calculate_volatility(prices)
    assert vol is not None
    assert vol > 0


def test_calculate_max_drawdown() -> None:
    prices = [100.0, 120.0, 90.0, 110.0]
    # Peak is 120.0, drops to 90.0 -> (120 - 90) / 120 = 25.0%
    assert calculate_max_drawdown(prices) == 25.0


def test_calculate_returns() -> None:
    prices = [100.0, 110.0, 125.0]
    assert calculate_returns(prices) == 25.0


def test_compute_technical_indicators_bundle() -> None:
    prices = [float(100 + (i % 5) * 2) for i in range(40)]
    result = compute_technical_indicators(prices)
    assert "sma_20" in result
    assert "rsi_14" in result
    assert "macd" in result
    assert "volatility" in result
    assert "disclaimer" in result
