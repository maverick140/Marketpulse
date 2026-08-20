"""Macroeconomic data API schemas."""

from __future__ import annotations

import datetime as dt
from pydantic import BaseModel, Field


class MacroIndicatorResponse(BaseModel):
    indicator: str = Field(examples=["Inflation"])
    value: float = Field(examples=[4.8])
    unit: str = Field(examples=["percent"])
    period: str = Field(examples=["2024-05"])
    previous_value: float | None = Field(default=None, examples=[4.9])
    change: float | None = Field(default=None, examples=[-0.1])
    source: str = Field(examples=["Demo Macro Catalog"])
    provider: str = Field(examples=["demo"])
    data_status: str = Field(examples=["demo"])
    retrieved_at: dt.datetime | None = None


class MacroListResponse(BaseModel):
    indicators: list[MacroIndicatorResponse]
    count: int
    data_status: str = Field(examples=["demo"])
    retrieved_at: dt.datetime


class MacroHistoryPoint(BaseModel):
    period: str = Field(examples=["2024-01"])
    value: float = Field(examples=[5.1])
    date: dt.date | None = None


class MacroDetailResponse(BaseModel):
    indicator: str = Field(examples=["Inflation"])
    current: MacroIndicatorResponse
    history: list[MacroHistoryPoint]
    data_status: str = Field(examples=["demo"])
