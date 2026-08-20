"""Sentiment analysis API schemas."""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class TextSentimentRequest(BaseModel):
    text: str = Field(examples=["Quarterly revenues beat consensus with robust cloud expansion."])


class SentimentDetailResponse(BaseModel):
    score: float = Field(examples=[0.75])
    label: str = Field(examples=["positive"])
    confidence: float = Field(examples=[0.88])
    positive_count: int = 2
    negative_count: int = 0
    total_tokens: int = 8
    model: str = "Financial Lexicon v1"
    version: str = "1.0.0"
    timestamp: datetime


class ArticleSentimentItem(BaseModel):
    id: str | None = None
    headline: str
    summary: str
    category: str
    score: float
    label: str
    confidence: float


class SymbolSentimentResponse(BaseModel):
    symbol: str
    average_score: float
    overall_label: str
    confidence: float
    article_count: int
    positive_articles: int
    neutral_articles: int
    negative_articles: int
    articles: list[ArticleSentimentItem]


class SectorSentimentItem(BaseModel):
    sector: str
    average_score: float
    label: str
    article_count: int


class SectorSentimentResponse(BaseModel):
    sectors: list[SectorSentimentItem]
    total_sectors: int


class SentimentTrendPoint(BaseModel):
    date: str
    score: float
    label: str
    count: int


class SentimentTrendsResponse(BaseModel):
    trends: list[SentimentTrendPoint]
    timeframe: str


class MarketSentimentResponse(BaseModel):
    overall_score: float
    overall_label: str
    confidence: float
    distribution: dict[str, int]
    total_articles: int
    sectors: list[SectorSentimentItem]
    recent_analyses: list[ArticleSentimentItem]
    generated_at: datetime
