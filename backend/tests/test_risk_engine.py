"""Unit tests for Risk and Scenario analytics math."""

from app.analytics.risk import (
    calculate_beta,
    calculate_composite_risk_score,
    calculate_correlation,
    classify_market_regime,
    simulate_scenario,
)


def test_calculate_beta() -> None:
    asset_rets = [0.01, 0.02, -0.01, 0.03, -0.02, 0.015]
    bench_rets = [0.005, 0.01, -0.005, 0.015, -0.01, 0.008]
    beta = calculate_beta(asset_rets, bench_rets)
    assert beta is not None
    assert beta > 1.5  # Asset moved ~2x benchmark


def test_calculate_correlation() -> None:
    series_a = [10.0, 12.0, 14.0, 16.0, 18.0]
    series_b = [100.0, 120.0, 140.0, 160.0, 180.0]
    corr = calculate_correlation(series_a, series_b)
    assert corr == 1.0


def test_classify_market_regime() -> None:
    # High volatility regime
    prices = [100.0 + i for i in range(20)]
    assert classify_market_regime(prices, volatility=35.0) == "HIGH_VOLATILITY"

    # Trending up regime
    assert classify_market_regime(prices, volatility=16.0) == "TRENDING_UP"

    # Short series
    assert classify_market_regime([10.0, 12.0]) == "UNCERTAIN"


def test_calculate_composite_risk_score() -> None:
    score, tier = calculate_composite_risk_score(
        volatility=15.0,
        max_drawdown=4.0,
        geopolitical_severity=30,
        sentiment_score=0.2,
    )
    assert 0 <= score <= 100
    assert tier in {"LOW", "MODERATE", "ELEVATED", "HIGH", "VERY_HIGH"}


def test_simulate_scenario() -> None:
    res = simulate_scenario("Oil Surge", magnitude=20.0, current_market_price=23000.0)
    assert res["scenario_type"] == "Oil Surge"
    assert res["magnitude"] == 20.0
    assert "Energy" in res["sector_impacts"]
    assert res["sector_impacts"]["Energy"] > 0  # Oil surge benefits energy
    assert "Educational simulation" in res["disclaimer"]
