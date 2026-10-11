"""Mathematical risk analytics and market regime detection."""

from __future__ import annotations

import math
from typing import Any, Literal

MarketRegime = Literal[
    "TRENDING_UP",
    "TRENDING_DOWN",
    "RANGE_BOUND",
    "HIGH_VOLATILITY",
    "LOW_VOLATILITY",
    "UNCERTAIN",
]

RiskTier = Literal["LOW", "MODERATE", "ELEVATED", "HIGH", "VERY_HIGH"]


def calculate_beta(asset_returns: list[float], benchmark_returns: list[float]) -> float | None:
    if len(asset_returns) < 5 or len(asset_returns) != len(benchmark_returns):
        return 1.0

    mean_a = sum(asset_returns) / len(asset_returns)
    mean_b = sum(benchmark_returns) / len(benchmark_returns)

    covariance = sum((a - mean_a) * (b - mean_b) for a, b in zip(asset_returns, benchmark_returns)) / len(asset_returns)
    variance_b = sum((b - mean_b) ** 2 for b in benchmark_returns) / len(benchmark_returns)

    if variance_b == 0:
        return 1.0
    return round(covariance / variance_b, 2)


def calculate_correlation(series_a: list[float], series_b: list[float]) -> float | None:
    if len(series_a) < 3 or len(series_a) != len(series_b):
        return None

    mean_a = sum(series_a) / len(series_a)
    mean_b = sum(series_b) / len(series_b)

    num = sum((a - mean_a) * (b - mean_b) for a, b in zip(series_a, series_b))
    den_a = math.sqrt(sum((a - mean_a) ** 2 for a in series_a))
    den_b = math.sqrt(sum((b - mean_b) ** 2 for b in series_b))

    if den_a == 0 or den_b == 0:
        return 0.0
    return round(num / (den_a * den_b), 2)


def classify_market_regime(
    prices: list[float],
    volatility: float | None = None,
) -> MarketRegime:
    if len(prices) < 10:
        return "UNCERTAIN"

    # Moving averages
    sma_short = sum(prices[-5:]) / 5
    sma_long = sum(prices[-10:]) / 10
    total_change = (prices[-1] - prices[0]) / prices[0]

    vol = volatility if volatility is not None else 18.0

    if vol > 30.0:
        return "HIGH_VOLATILITY"
    if vol < 12.0 and abs(total_change) < 0.02:
        return "LOW_VOLATILITY"
    if sma_short > sma_long and total_change > 0.02:
        return "TRENDING_UP"
    if sma_short < sma_long and total_change < -0.02:
        return "TRENDING_DOWN"
    return "RANGE_BOUND"


def calculate_composite_risk_score(
    volatility: float | None,
    max_drawdown: float | None,
    geopolitical_severity: int = 50,
    sentiment_score: float = 0.0,
) -> tuple[int, RiskTier]:
    """Compute transparent 0-100 risk score based on volatility, drawdown, geopolitics, and sentiment."""
    vol = volatility if volatility is not None else 18.0
    dd = max_drawdown if max_drawdown is not None else 5.0

    # Weight components
    # Volatility component (0-35 points) - scaled from 0% to 50% vol
    vol_pts = min((vol / 50.0) * 35.0, 35.0)

    # Drawdown component (0-25 points) - scaled from 0% to 30% dd
    dd_pts = min((dd / 30.0) * 25.0, 25.0)

    # Geopolitical component (0-25 points)
    geo_pts = (geopolitical_severity / 100.0) * 25.0

    # Negative sentiment penalty (0-15 points)
    sent_penalty = max(-sentiment_score, 0.0) * 15.0

    total_score = int(round(vol_pts + dd_pts + geo_pts + sent_penalty))
    score = max(0, min(total_score, 100))

    if score <= 20:
        tier: RiskTier = "LOW"
    elif score <= 40:
        tier = "MODERATE"
    elif score <= 60:
        tier = "ELEVATED"
    elif score <= 80:
        tier = "HIGH"
    else:
        tier = "VERY_HIGH"

    return score, tier


def simulate_scenario(
    scenario_type: str,
    magnitude: float,
    current_market_price: float = 23200.0,
) -> dict[str, Any]:
    """Simulate macroeconomic/geopolitical shock scenario on sectors and assets."""
    # Sector impact sensitivities
    # e.g., Oil shock: Energy (+), Technology (-), Financials (-), Consumer (-)
    st = scenario_type.upper()

    if "OIL" in st:
        multiplier = magnitude / 100.0
        impacts = {
            "Energy": round(magnitude * 0.65, 2),
            "Financials": round(-magnitude * 0.35, 2),
            "Consumer Goods": round(-magnitude * 0.45, 2),
            "Technology": round(-magnitude * 0.15, 2),
            "Industrials": round(-magnitude * 0.30, 2),
        }
        market_est = round(-magnitude * 0.25, 2)
        summary = f"Simulated {magnitude:+g}% Crude Oil shock scenario. Energy names exhibit positive correlation while transport and consumption face cost headwinds."

    elif "RATE" in st or "INTEREST" in st:
        bps = magnitude
        impacts = {
            "Financials": round(bps * 0.03, 2),
            "Technology": round(-bps * 0.06, 2),
            "Industrials": round(-bps * 0.04, 2),
            "Consumer Goods": round(-bps * 0.03, 2),
            "Energy": round(-bps * 0.02, 2),
        }
        market_est = round(-bps * 0.035, 2)
        summary = f"Simulated {magnitude:+g} bps policy rate shift. Financial margins expand moderately while long-duration growth multiples compress."

    elif "GEO" in st or "TARIFF" in st or "CONFLICT" in st:
        impacts = {
            "Technology": round(-magnitude * 0.40, 2),
            "Financials": round(-magnitude * 0.30, 2),
            "Energy": round(magnitude * 0.50, 2),
            "Industrials": round(-magnitude * 0.35, 2),
            "Consumer Goods": round(-magnitude * 0.20, 2),
        }
        market_est = round(-magnitude * 0.30, 2)
        summary = f"Simulated {magnitude:+g}% geopolitical supply disruption scenario. Safe-haven energy assets gain while cross-border trade equities face supply friction."

    else:
        # Generic market shock
        impacts = {
            "Technology": round(magnitude * 1.10, 2),
            "Financials": round(magnitude * 1.05, 2),
            "Energy": round(magnitude * 0.90, 2),
            "Industrials": round(magnitude * 0.95, 2),
            "Consumer Goods": round(magnitude * 0.70, 2),
        }
        market_est = round(magnitude, 2)
        summary = f"Simulated broad market equity shock of {magnitude:+g}%. Higher beta sectors experience amplified price sensitivity."

    simulated_price = round(current_market_price * (1 + market_est / 100.0), 2)

    return {
        "scenario_type": scenario_type,
        "magnitude": magnitude,
        "estimated_market_impact_percent": market_est,
        "simulated_market_price": simulated_price,
        "sector_impacts": impacts,
        "summary": summary,
        "disclaimer": "Educational simulation for risk exploration only. Not a predictive forecast.",
    }
