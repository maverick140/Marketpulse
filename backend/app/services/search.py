"""Unified Search service layer across all MarketPulse intelligence domains."""

from __future__ import annotations

from datetime import datetime, timezone

from app.schemas.search import SearchResultItem, UnifiedSearchResponse
from app.services.announcements import list_announcements
from app.services.geopolitics import list_geopolitical_events
from app.services.macro import list_macro_indicators
from app.services.markets import get_market_overview, search_securities
from app.services.news import list_news


def perform_unified_search(query: str) -> UnifiedSearchResponse:
    q = query.strip()
    if not q:
        return UnifiedSearchResponse(
            query=query,
            total_results=0,
            markets=[],
            macro=[],
            news=[],
            geopolitics=[],
            announcements=[],
            generated_at=datetime.now(timezone.utc),
        )

    q_lower = q.lower()

    # 1. Search Markets
    market_matches = search_securities(q).results
    markets_items = [
        SearchResultItem(
            category="Markets",
            title=f"{m.symbol} — {m.name}",
            subtitle=f"Price: ₹{m.price:.2f} | Sector: {m.sector or 'Equities'}",
            identifier=m.symbol,
            data_status="demo",
        )
        for m in market_matches[:6]
    ]

    # 2. Search Macro
    macro_data = list_macro_indicators().indicators
    macro_items = [
        SearchResultItem(
            category="Macro",
            title=m.indicator,
            subtitle=f"Value: {m.value} {m.unit} (Period: {m.period})",
            identifier=m.indicator,
            data_status=m.data_status,
        )
        for m in macro_data
        if q_lower in m.indicator.lower() or q_lower in m.unit.lower()
    ]

    # 3. Search News
    news_res = list_news(q=q, page=1, page_size=6).articles
    news_items = [
        SearchResultItem(
            category="News",
            title=a.headline,
            subtitle=f"{a.category} | {a.source}",
            identifier=a.id or a.headline,
            data_status=a.data_status,
        )
        for a in news_res
    ]

    # 4. Search Geopolitics
    geo_res = list_geopolitical_events().events
    geo_items = [
        SearchResultItem(
            category="Geopolitics",
            title=e.title,
            subtitle=f"{e.region} ({e.country}) | Severity: {e.severity_label}",
            identifier=e.id or e.title,
            data_status=e.data_status,
        )
        for e in geo_res
        if q_lower in e.title.lower()
        or (e.description and q_lower in e.description.lower())
        or q_lower in e.country.lower()
        or q_lower in e.region.lower()
        or any(q_lower in sec.lower() for sec in e.related_sectors)
    ]

    # 5. Search Announcements
    ann_res = list_announcements().announcements
    ann_items = [
        SearchResultItem(
            category="Announcements",
            title=an.title,
            subtitle=f"{an.category} | {an.announcement_type}",
            identifier=an.id or an.title,
            data_status=an.data_status,
        )
        for an in ann_res
        if q_lower in an.title.lower()
        or q_lower in an.category.lower()
        or any(q_lower in ent.lower() for ent in an.related_entities)
    ]

    total = len(markets_items) + len(macro_items) + len(news_items) + len(geo_items) + len(ann_items)

    return UnifiedSearchResponse(
        query=query,
        total_results=total,
        markets=markets_items,
        macro=macro_items,
        news=news_items,
        geopolitics=geo_items,
        announcements=ann_items,
        generated_at=datetime.now(timezone.utc),
    )
