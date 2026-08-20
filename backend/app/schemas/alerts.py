"""Alerts and Real-time Monitoring schemas."""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class AlertItem(BaseModel):
    id: str
    alert_type: str = Field(examples=["PRICE_SPIKE", "VOLUME_ANOMALY", "GEOPOLITICAL_RISK", "MACRO_RELEASE"])
    severity: str = Field(examples=["INFO", "WARNING", "CRITICAL"])
    entity: str = Field(examples=["RELIANCE", "NIFTY 50", "Inflation", "Middle East"])
    message: str = Field(examples=["Intraday price expansion exceeded 0.60%"])
    explanation: str = Field(examples=["Volume participation increased with positive software sector sentiment."])
    dedup_key: str
    timestamp: datetime
    data_status: str = "demo"


class AlertListResponse(BaseModel):
    alerts: list[AlertItem]
    total: int
    critical_count: int
    warning_count: int
    info_count: int
    generated_at: datetime
