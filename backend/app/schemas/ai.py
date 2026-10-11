"""AI Research & Intelligence API schemas."""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class AIResearchRequest(BaseModel):
    query: str = Field(
        examples=["What is the current outlook on the Indian technology sector considering macro and geopolitics?"]
    )
    symbol: str | None = Field(default=None, examples=["INFY"])
    sector: str | None = Field(default=None, examples=["Technology"])


class AIEvidenceItem(BaseModel):
    source_type: str = Field(examples=["market_data", "news", "macro", "geopolitics", "sentiment"])
    reference: str = Field(examples=["NIFTY IT (+0.42%)", "Inflation (4.8%)"])
    note: str = Field(examples=["Positive momentum in software services supported by resilient earnings."])


class AIInsightResponse(BaseModel):
    query: str
    summary: str
    market_context: str
    macro_factors: list[str]
    news_factors: list[str]
    sentiment: str
    geopolitical_factors: list[str]
    risk_factors: list[str]
    uncertainties: list[str]
    evidence: list[AIEvidenceItem]
    model: str = "MarketPulse Hybrid Analyst v1"
    generated_at: datetime
    disclaimer: str = Field(
        default=(
            "Educational and research demonstration only. Not investment advice, "
            "trading recommendation, or financial counsel. Models may produce inaccuracies."
        )
    )


class AIInsightsListResponse(BaseModel):
    insights: list[AIInsightResponse]
    total: int
    data_status: str = "demo"
    generated_at: datetime
