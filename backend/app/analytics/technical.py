"""Educational financial analytics and technical indicators.

All calculations are for educational and demonstration purposes only.
They must not be converted into automated investment or trading recommendations.
"""

from __future__ import annotations

import math
from typing import Any


def calculate_sma(prices: list[float], window: int) -> float | None:
    if len(prices) < window or window <= 0:
        return None
    subset = prices[-window:]
    return round(sum(subset) / window, 2)


def calculate_ema(prices: list[float], window: int) -> float | None:
    if len(prices) < window or window <= 0:
        return None
    multiplier = 2.0 / (window + 1)
    ema = sum(prices[:window]) / window
    for price in prices[window:]:
        ema = (price - ema) * multiplier + ema
    return round(ema, 2)


def calculate_rsi(prices: list[float], period: int = 14) -> float | None:
    if len(prices) <= period:
        return None

    gains: list[float] = []
    losses: list[float] = []

    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        if change >= 0:
            gains.append(change)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(change))

    if len(gains) < period:
        return None

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return round(rsi, 2)


def calculate_macd(
    prices: list[float],
    fast: int = 12,
    slow: int = 26,
    signal_period: int = 9,
) -> dict[str, float | None]:
    if len(prices) < slow + signal_period:
        return {"macd_line": None, "signal_line": None, "histogram": None}

    # Calculate fast and slow EMAs across price series
    fast_multiplier = 2.0 / (fast + 1)
    slow_multiplier = 2.0 / (slow + 1)

    fast_ema = sum(prices[:fast]) / fast
    slow_ema = sum(prices[:slow]) / slow

    macd_series: list[float] = []

    for i, price in enumerate(prices):
        if i >= fast:
            fast_ema = (price - fast_ema) * fast_multiplier + fast_ema
        if i >= slow:
            slow_ema = (price - slow_ema) * slow_multiplier + slow_ema
            macd_series.append(fast_ema - slow_ema)

    if len(macd_series) < signal_period:
        return {"macd_line": None, "signal_line": None, "histogram": None}

    signal_multiplier = 2.0 / (signal_period + 1)
    signal_ema = sum(macd_series[:signal_period]) / signal_period
    for macd_val in macd_series[signal_period:]:
        signal_ema = (macd_val - signal_ema) * signal_multiplier + signal_ema

    current_macd = macd_series[-1]
    histogram = current_macd - signal_ema

    return {
        "macd_line": round(current_macd, 2),
        "signal_line": round(signal_ema, 2),
        "histogram": round(histogram, 2),
    }


def calculate_volatility(prices: list[float]) -> float | None:
    """Calculate annualized volatility from daily closing price returns."""
    if len(prices) < 2:
        return None

    returns: list[float] = []
    for i in range(1, len(prices)):
        if prices[i - 1] > 0:
            returns.append((prices[i] - prices[i - 1]) / prices[i - 1])

    if not returns:
        return None

    mean_return = sum(returns) / len(returns)
    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
    daily_std = math.sqrt(variance)
    annualized = daily_std * math.sqrt(252) * 100.0
    return round(annualized, 2)


def calculate_max_drawdown(prices: list[float]) -> float | None:
    if len(prices) < 2:
        return None

    peak = prices[0]
    max_dd = 0.0

    for price in prices:
        if price > peak:
            peak = price
        elif peak > 0:
            dd = (peak - price) / peak
            if dd > max_dd:
                max_dd = dd

    return round(max_dd * 100.0, 2)


def calculate_returns(prices: list[float]) -> float | None:
    if len(prices) < 2 or prices[0] <= 0:
        return None
    ret = ((prices[-1] - prices[0]) / prices[0]) * 100.0
    return round(ret, 2)


def compute_technical_indicators(prices: list[float]) -> dict[str, Any]:
    """Compute standard educational indicators dictionary from a list of prices."""
    if not prices:
        return {
            "sma_20": None,
            "sma_50": None,
            "ema_20": None,
            "rsi_14": None,
            "macd": {"macd_line": None, "signal_line": None, "histogram": None},
            "volatility": None,
            "max_drawdown": None,
            "period_return": None,
            "disclaimer": "Educational demonstration only. Not financial advice.",
        }

    return {
        "sma_20": calculate_sma(prices, 20),
        "sma_50": calculate_sma(prices, 50),
        "ema_20": calculate_ema(prices, 20),
        "rsi_14": calculate_rsi(prices, 14),
        "macd": calculate_macd(prices),
        "volatility": calculate_volatility(prices),
        "max_drawdown": calculate_max_drawdown(prices),
        "period_return": calculate_returns(prices),
        "disclaimer": "Educational demonstration only. Not financial advice.",
    }
