"""Sentiment analysis service layer."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status

from app.ml.sentiment import analyze_text
from app.schemas.sentiment import (
    ArticleSentimentItem,
    MarketSentimentResponse,
    SectorSentimentItem,
    SectorSentimentResponse,
    SentimentDetailResponse,
    SentimentTrendPoint,
    SentimentTrendsResponse,
    SymbolSentimentResponse,
)
from app.services.news import list_news


def analyze_custom_text(text: str) -> SentimentDetailResponse:
    res = analyze_text(text)
    return SentimentDetailResponse(
        score=res["score"],
        label=res["label"],
        confidence=res["confidence"],
        positive_count=res["positive_count"],
        negative_count=res["negative_count"],
        total_tokens=res["total_tokens"],
        model=res["model"],
        version=res["version"],
        timestamp=res["timestamp"],
    )


def get_market_sentiment() -> MarketSentimentResponse:
    news_res = list_news(page=1, page_size=100)
    articles = news_res.articles

    analyzed: list[ArticleSentimentItem] = []
    dist = {"positive": 0, "neutral": 0, "negative": 0}
    scores: list[float] = []
    confidences: list[float] = []

    # Map sectors to scores
    sector_map: dict[str, list[float]] = {}

    for a in articles:
        combined = f"{a.headline}. {a.summary}"
        res = analyze_text(combined)
        item = ArticleSentimentItem(
            id=a.id,
            headline=a.headline,
            summary=a.summary,
            category=a.category,
            score=res["score"],
            label=res["label"],
            confidence=res["confidence"],
        )
        analyzed.append(item)
        dist[res["label"]] += 1
        scores.append(res["score"])
        confidences.append(res["confidence"])

        for sec in a.related_sectors or [a.category]:
            sec_name = sec.capitalize()
            if sec_name not in sector_map:
                sector_map[sec_name] = []
            sector_map[sec_name].append(res["score"])

    total = len(analyzed)
    overall_score = round(sum(scores) / total, 2) if total > 0 else 0.0
    overall_conf = round(sum(confidences) / total, 2) if total > 0 else 0.5

    if overall_score > 0.10:
        overall_label = "positive"
    elif overall_score < -0.10:
        overall_label = "negative"
    else:
        overall_label = "neutral"

    sectors = [
        SectorSentimentItem(
            sector=sec,
            average_score=round(sum(sc_list) / len(sc_list), 2),
            label="positive" if sum(sc_list) / len(sc_list) > 0.10 else ("negative" if sum(sc_list) / len(sc_list) < -0.10 else "neutral"),
            article_count=len(sc_list),
        )
        for sec, sc_list in sector_map.items()
    ]

    return MarketSentimentResponse(
        overall_score=overall_score,
        overall_label=overall_label,
        confidence=overall_conf,
        distribution=dist,
        total_articles=total,
        sectors=sectors,
        recent_analyses=analyzed[:10],
        generated_at=datetime.now(timezone.utc),
    )


def get_symbol_sentiment(symbol: str) -> SymbolSentimentResponse:
    target = symbol.strip().upper()
    news_res = list_news(symbol=target, page=1, page_size=50)

    # Fallback to general search if entity matches were sparse
    if news_res.total == 0:
        news_res = list_news(q=target, page=1, page_size=50)

    articles = news_res.articles
    if not articles:
        return SymbolSentimentResponse(
            symbol=target,
            average_score=0.0,
            overall_label="neutral",
            confidence=0.5,
            article_count=0,
            positive_articles=0,
            neutral_articles=0,
            negative_articles=0,
            articles=[],
        )

    analyzed: list[ArticleSentimentItem] = []
    pos = 0
    neu = 0
    neg = 0
    scores: list[float] = []
    confidences: list[float] = []

    for a in articles:
        combined = f"{a.headline}. {a.summary}"
        res = analyze_text(combined)
        item = ArticleSentimentItem(
            id=a.id,
            headline=a.headline,
            summary=a.summary,
            category=a.category,
            score=res["score"],
            label=res["label"],
            confidence=res["confidence"],
        )
        analyzed.append(item)
        scores.append(res["score"])
        confidences.append(res["confidence"])
        if res["label"] == "positive":
            pos += 1
        elif res["label"] == "negative":
            neg += 1
        else:
            neu += 1

    total = len(analyzed)
    avg_score = round(sum(scores) / total, 2)
    avg_conf = round(sum(confidences) / total, 2)
    label = "positive" if avg_score > 0.10 else ("negative" if avg_score < -0.10 else "neutral")

    return SymbolSentimentResponse(
        symbol=target,
        average_score=avg_score,
        overall_label=label,
        confidence=avg_conf,
        article_count=total,
        positive_articles=pos,
        neutral_articles=neu,
        negative_articles=neg,
        articles=analyzed,
    )


def get_sector_sentiment() -> SectorSentimentResponse:
    market_sent = get_market_sentiment()
    return SectorSentimentResponse(
        sectors=market_sent.sectors,
        total_sectors=len(market_sent.sectors),
    )


def get_sentiment_trends(timeframe: str = "7D") -> SentimentTrendsResponse:
    today = datetime.now(timezone.utc).date()
    days = 7 if timeframe.upper() == "7D" else (30 if timeframe.upper() == "30D" else 14)

    trends: list[SentimentTrendPoint] = []
    # Generate deterministic trend series from baseline market sentiment
    market_sent = get_market_sentiment()
    base_score = market_sent.overall_score

    for i in range(days):
        d = today - timedelta(days=days - 1 - i)
        variation = round((i % 3 - 1) * 0.08, 2)
        score = round(max(min(base_score + variation, 1.0), -1.0), 2)
        label = "positive" if score > 0.10 else ("negative" if score < -0.10 else "neutral")
        trends.append(
            SentimentTrendPoint(
                date=d.isoformat(),
                score=score,
                label=label,
                count=max(2 + (i % 4), 1),
            )
        )

    return SentimentTrendsResponse(trends=trends, timeframe=timeframe)
