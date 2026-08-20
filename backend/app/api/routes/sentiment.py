"""Sentiment analysis API routes."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.schemas.sentiment import (
    MarketSentimentResponse,
    SectorSentimentResponse,
    SentimentDetailResponse,
    SentimentTrendsResponse,
    SymbolSentimentResponse,
    TextSentimentRequest,
)
from app.services.sentiment import (
    analyze_custom_text,
    get_market_sentiment,
    get_sector_sentiment,
    get_sentiment_trends,
    get_symbol_sentiment,
)

router = APIRouter(tags=["sentiment"])


@router.get("", response_model=MarketSentimentResponse)
def market_sentiment() -> MarketSentimentResponse:
    """Retrieve aggregate market sentiment, distribution, and sector breakdown."""
    return get_market_sentiment()


@router.get("/symbol/{symbol}", response_model=SymbolSentimentResponse)
def symbol_sentiment(symbol: str) -> SymbolSentimentResponse:
    """Retrieve sentiment breakdown and analyzed articles for a specific symbol."""
    return get_symbol_sentiment(symbol)


@router.get("/sectors", response_model=SectorSentimentResponse)
def sectors_sentiment() -> SectorSentimentResponse:
    """Retrieve sector-level sentiment aggregation."""
    return get_sector_sentiment()


@router.get("/trends", response_model=SentimentTrendsResponse)
def sentiment_trends(
    timeframe: str = Query(default="7D", description="Trend timeframe (e.g. 7D, 14D, 30D)"),
) -> SentimentTrendsResponse:
    """Retrieve historical sentiment trends over specified duration."""
    return get_sentiment_trends(timeframe)


@router.post("/analyze", response_model=SentimentDetailResponse)
def analyze_text_endpoint(payload: TextSentimentRequest) -> SentimentDetailResponse:
    """Analyze sentiment of arbitrary financial text snippet."""
    return analyze_custom_text(payload.text)
