"""Risk Intelligence and Scenario Lab service layer."""

from __future__ import annotations

from datetime import datetime, timezone

from app.analytics.risk import (
    calculate_beta,
    calculate_composite_risk_score,
    calculate_correlation,
    classify_market_regime,
    simulate_scenario,
)
from app.analytics.technical import calculate_max_drawdown, calculate_volatility
from app.schemas.risk import (
    CorrelationMatrixResponse,
    RiskOverviewResponse,
    ScenarioRequest,
    ScenarioResponse,
    SecurityRiskResponse,
)
from app.services.geopolitics import list_geopolitical_events
from app.services.markets import get_history, get_market_overview
from app.services.sentiment import get_market_sentiment


def get_risk_overview() -> RiskOverviewResponse:
    overview = get_market_overview()
    geo = list_geopolitical_events()
    sentiment = get_market_sentiment()

    # Get Nifty 50 history
    nifty_hist = get_history("NIFTY 50", "1M")
    closes = [p.close for p in nifty_hist.points]

    vol = calculate_volatility(closes) or 16.5
    dd = calculate_max_drawdown(closes) or 4.2
    regime = classify_market_regime(closes, vol)

    top_geo_sev = geo.events[0].severity if geo.events else 45
    score, tier = calculate_composite_risk_score(
        volatility=vol,
        max_drawdown=dd,
        geopolitical_severity=top_geo_sev,
        sentiment_score=sentiment.overall_score,
    )

    top_drivers = [
        f"Realized 30-day annualized volatility measured at {vol:.1f}%.",
        f"Regional geopolitical posture categorized at {geo.events[0].severity_label if geo.events else 'MODERATE'} severity.",
        f"Media narrative reflects {sentiment.overall_label} tone (score: {sentiment.overall_score:+.2f}).",
    ]

    sector_risks = {
        "Technology": max(20, min(score - 4, 90)),
        "Energy": max(20, min(score + 8, 90)),
        "Financials": max(20, min(score + 2, 90)),
        "Consumer Goods": max(20, min(score - 10, 90)),
        "Industrials": max(20, min(score + 5, 90)),
    }

    return RiskOverviewResponse(
        market_risk_score=score,
        risk_tier=tier,
        market_regime=regime,
        volatility_index=vol,
        top_drivers=top_drivers,
        sector_risks=sector_risks,
        generated_at=datetime.now(timezone.utc),
    )


def get_security_risk(symbol: str) -> SecurityRiskResponse:
    target = symbol.strip().upper()
    hist = get_history(target, "1M")
    nifty_hist = get_history("NIFTY 50", "1M")

    asset_closes = [p.close for p in hist.points]
    bench_closes = [p.close for p in nifty_hist.points]

    vol = calculate_volatility(asset_closes) or 22.0
    dd = calculate_max_drawdown(asset_closes) or 6.5
    regime = classify_market_regime(asset_closes, vol)

    asset_rets = [
        (asset_closes[i] - asset_closes[i - 1]) / asset_closes[i - 1]
        for i in range(1, len(asset_closes))
    ] if len(asset_closes) > 1 else []

    bench_rets = [
        (bench_closes[i] - bench_closes[i - 1]) / bench_closes[i - 1]
        for i in range(1, len(bench_closes))
    ] if len(bench_closes) > 1 else []

    beta = calculate_beta(asset_rets, bench_rets) or 1.05

    # Volume anomaly ratio: compare latest candle volume with average volume
    volumes = [p.volume for p in hist.points if p.volume > 0]
    if volumes and len(volumes) > 1:
        avg_vol = sum(volumes[:-1]) / (len(volumes) - 1)
        vol_ratio = round(volumes[-1] / max(avg_vol, 1.0), 2)
    else:
        vol_ratio = 1.0

    score, tier = calculate_composite_risk_score(
        volatility=vol,
        max_drawdown=dd,
        geopolitical_severity=45,
        sentiment_score=0.1,
    )

    return SecurityRiskResponse(
        symbol=target,
        risk_score=score,
        risk_tier=tier,
        beta=beta,
        volatility=vol,
        max_drawdown=dd,
        regime=regime,
        volume_anomaly_ratio=vol_ratio,
    )


def run_scenario_simulation(req: ScenarioRequest) -> ScenarioResponse:
    res = simulate_scenario(
        scenario_type=req.scenario_type,
        magnitude=req.magnitude,
        current_market_price=23210.45,
    )
    return ScenarioResponse(
        scenario_type=res["scenario_type"],
        magnitude=res["magnitude"],
        estimated_market_impact_percent=res["estimated_market_impact_percent"],
        simulated_market_price=res["simulated_market_price"],
        sector_impacts=res["sector_impacts"],
        summary=res["summary"],
        disclaimer=res["disclaimer"],
    )


def get_correlation_matrix() -> CorrelationMatrixResponse:
    assets = ["NIFTY 50", "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]
    histories = {a: [p.close for p in get_history(a, "1M").points] for a in assets}

    matrix: list[list[float]] = []
    for a in assets:
        row: list[float] = []
        for b in assets:
            if a == b:
                row.append(1.0)
            else:
                corr = calculate_correlation(histories[a], histories[b])
                row.append(corr if corr is not None else 0.5)
        matrix.append(row)

    return CorrelationMatrixResponse(
        assets=assets,
        matrix=matrix,
        generated_at=datetime.now(timezone.utc),
    )
