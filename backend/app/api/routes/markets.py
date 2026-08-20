"""Market data API routes."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.schemas.markets import (
    MarketHistoryResponse,
    MarketOverviewResponse,
    MarketQuoteResponse,
    SecuritySearchResponse,
    TechnicalIndicatorsResponse,
)
from app.services.markets import (
    get_history,
    get_indicators,
    get_market_overview,
    get_quote,
    search_securities,
)

router = APIRouter(tags=["markets"])


@router.get("/overview", response_model=MarketOverviewResponse)
def market_overview() -> MarketOverviewResponse:
    """Retrieve market summary including indices, top gainers, decliners, and active."""
    return get_market_overview()


@router.get("/search", response_model=SecuritySearchResponse)
def search(q: str = Query(default="", description="Search query string")) -> SecuritySearchResponse:
    """Search securities by symbol, company name, or sector."""
    return search_securities(q)


@router.get("/quote/{symbol}", response_model=MarketQuoteResponse)
def quote(symbol: str) -> MarketQuoteResponse:
    """Retrieve detailed market quote for a specific security."""
    return get_quote(symbol)


@router.get("/history/{symbol}", response_model=MarketHistoryResponse)
def history(
    symbol: str,
    timeframe: str = Query(
        default="1M",
        description="Historical timeframe: 1D, 5D, 1M, 3M, 6M, 1Y",
    ),
) -> MarketHistoryResponse:
    """Retrieve historical OHLCV price series for a specific security."""
    return get_history(symbol, timeframe)


@router.get("/indicators/{symbol}", response_model=TechnicalIndicatorsResponse)
def indicators(
    symbol: str,
    timeframe: str = Query(
        default="1M",
        description="Historical timeframe: 1D, 5D, 1M, 3M, 6M, 1Y",
    ),
) -> TechnicalIndicatorsResponse:
    """Retrieve educational technical indicators (SMA, EMA, RSI, MACD, Volatility, Drawdown)."""
    return get_indicators(symbol, timeframe)
