"""Risk and Scenario Lab API schemas."""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class ScenarioRequest(BaseModel):
    scenario_type: str = Field(
        default="Crude Oil Surge",
        examples=["Crude Oil Surge", "Interest Rate Hike", "Geopolitical Disruption", "Broad Market Correction"],
    )
    magnitude: float = Field(
        default=15.0,
        examples=[15.0, -5.0, 50.0],
        description="Percentage shock magnitude (or basis points for interest rates)",
    )


class ScenarioResponse(BaseModel):
    scenario_type: str
    magnitude: float
    estimated_market_impact_percent: float
    simulated_market_price: float
    sector_impacts: dict[str, float]
    summary: str
    disclaimer: str = Field(
        default="Educational simulation for risk exploration only. Not a predictive forecast."
    )


class SecurityRiskResponse(BaseModel):
    symbol: str
    risk_score: int = Field(examples=[42])
    risk_tier: str = Field(examples=["ELEVATED"])
    beta: float = Field(examples=[1.15])
    volatility: float = Field(examples=[22.4])
    max_drawdown: float = Field(examples=[8.5])
    regime: str = Field(examples=["TRENDING_UP"])
    volume_anomaly_ratio: float = Field(examples=[1.2])


class CorrelationMatrixResponse(BaseModel):
    assets: list[str]
    matrix: list[list[float]]
    generated_at: datetime


class RiskOverviewResponse(BaseModel):
    market_risk_score: int = Field(examples=[38])
    risk_tier: str = Field(examples=["MODERATE"])
    market_regime: str = Field(examples=["TRENDING_UP"])
    volatility_index: float = Field(examples=[16.8])
    top_drivers: list[str]
    sector_risks: dict[str, int]
    generated_at: datetime
