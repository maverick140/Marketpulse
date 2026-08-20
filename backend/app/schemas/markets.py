"""Market data API schemas."""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class MarketQuoteResponse(BaseModel):
    symbol: str = Field(examples=["RELIANCE"])
    name: str = Field(examples=["Reliance Industries Ltd (demo)"])
    price: float = Field(examples=[2912.50])
    change: float | None = Field(default=None, examples=[18.40])
    change_percent: float | None = Field(default=None, examples=[0.64])
    volume: int | None = Field(default=None, examples=[4250000])
    timestamp: datetime
    provider: str = Field(examples=["demo"])
    data_status: str = Field(examples=["demo"])
    source: str | None = None
    source_url: str | None = None
    sector: str | None = Field(default=None, examples=["Energy"])
    retrieved_at: datetime | None = None


class MarketIndexResponse(BaseModel):
    symbol: str = Field(examples=["NIFTY 50"])
    name: str = Field(examples=["NIFTY 50"])
    value: float = Field(examples=[23210.45])
    change: float | None = Field(default=None, examples=[84.20])
    change_percent: float | None = Field(default=None, examples=[0.36])
    timestamp: datetime
    provider: str = Field(examples=["demo"])
    data_status: str = Field(examples=["demo"])
    source: str | None = None


class MarketOverviewResponse(BaseModel):
    indices: list[MarketIndexResponse]
    gainers: list[MarketQuoteResponse]
    decliners: list[MarketQuoteResponse]
    most_active: list[MarketQuoteResponse]
    data_status: str = Field(examples=["demo"])
    retrieved_at: datetime


class HistoricalPoint(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int = 0


class MarketHistoryResponse(BaseModel):
    symbol: str = Field(examples=["TCS"])
    timeframe: str = Field(examples=["1M"])
    data_status: str = Field(examples=["demo"])
    provider: str = Field(examples=["demo"])
    points: list[HistoricalPoint]


class MACDResponse(BaseModel):
    macd_line: float | None = None
    signal_line: float | None = None
    histogram: float | None = None


class TechnicalIndicatorsResponse(BaseModel):
    symbol: str = Field(examples=["INFY"])
    timeframe: str = Field(examples=["1M"])
    sma_20: float | None = None
    sma_50: float | None = None
    ema_20: float | None = None
    rsi_14: float | None = None
    macd: MACDResponse
    volatility: float | None = None
    max_drawdown: float | None = None
    period_return: float | None = None
    disclaimer: str = Field(
        default="Educational demonstration only. Not investment advice or trading recommendation."
    )


class SecuritySearchItem(BaseModel):
    symbol: str
    name: str
    sector: str | None = None
    price: float
    change_percent: float | None = None
    provider: str


class SecuritySearchResponse(BaseModel):
    query: str
    results: list[SecuritySearchItem]
    count: int
