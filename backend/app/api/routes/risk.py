"""Risk Intelligence and Scenario Lab API routes."""

from __future__ import annotations

from fastapi import APIRouter

from app.schemas.risk import (
    CorrelationMatrixResponse,
    RiskOverviewResponse,
    ScenarioRequest,
    ScenarioResponse,
    SecurityRiskResponse,
)
from app.services.risk import (
    get_correlation_matrix,
    get_risk_overview,
    get_security_risk,
    run_scenario_simulation,
)

router = APIRouter(tags=["risk"])


@router.get("/overview", response_model=RiskOverviewResponse)
def risk_overview() -> RiskOverviewResponse:
    """Retrieve market-wide risk score, regime classification, and sector risk profiles."""
    return get_risk_overview()


@router.get("/symbol/{symbol}", response_model=SecurityRiskResponse)
def security_risk(symbol: str) -> SecurityRiskResponse:
    """Retrieve risk score, beta, drawdown, volatility, and volume anomaly for a security."""
    return get_security_risk(symbol)


@router.post("/scenario", response_model=ScenarioResponse)
def scenario_simulation(payload: ScenarioRequest) -> ScenarioResponse:
    """Simulate macroeconomic and geopolitical shock scenarios across market sectors."""
    return run_scenario_simulation(payload)


@router.get("/correlation", response_model=CorrelationMatrixResponse)
def correlation_matrix() -> CorrelationMatrixResponse:
    """Retrieve correlation matrix across major equity assets and indices."""
    return get_correlation_matrix()
