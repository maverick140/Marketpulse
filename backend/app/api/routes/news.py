"""News intelligence API routes."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.schemas.news import NewsArticleResponse, NewsListResponse
from app.services.news import get_news_article, list_news

router = APIRouter(tags=["news"])


@router.get("", response_model=NewsListResponse)
def get_all_news(
    q: str = Query(default="", description="Search query string"),
    category: str = Query(default="", description="News category filter"),
    symbol: str = Query(default="", description="Associated symbol filter"),
    country: str = Query(default="", description="Associated country filter"),
    freshness: str = Query(default="", description="Freshness level filter (CURRENT, RECENT, BACKGROUND, ALL)"),
    max_age_hours: float | None = Query(default=None, description="Maximum article age in hours"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
) -> NewsListResponse:
    """Retrieve normalized news feed with search, category/symbol/country/freshness filters, and pagination."""
    return list_news(
        q=q,
        category=category,
        symbol=symbol,
        country=country,
        freshness=freshness,
        max_age_hours=max_age_hours,
        page=page,
        page_size=page_size,
    )


@router.get("/search", response_model=NewsListResponse)
def search_news(
    q: str = Query(default="", description="Search query string"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> NewsListResponse:
    """Search news articles by query."""
    return list_news(q=q, page=page, page_size=page_size)


@router.get("/symbol/{symbol}", response_model=NewsListResponse)
def get_news_by_symbol(
    symbol: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> NewsListResponse:
    """Retrieve news articles associated with a specific equity symbol."""
    return list_news(symbol=symbol, page=page, page_size=page_size)


@router.get("/category/{category}", response_model=NewsListResponse)
def get_news_by_category(
    category: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> NewsListResponse:
    """Retrieve news articles belonging to a specific category."""
    return list_news(category=category, page=page, page_size=page_size)


@router.get("/country/{country}", response_model=NewsListResponse)
def get_news_by_country(
    country: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> NewsListResponse:
    """Retrieve news articles associated with a specific country."""
    return list_news(country=country, page=page, page_size=page_size)


@router.get("/{id}", response_model=NewsArticleResponse)
def get_single_news(id: str) -> NewsArticleResponse:
    """Retrieve a single news article by ID or content hash."""
    return get_news_article(id)
