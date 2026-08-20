"""News intelligence service layer with dynamic freshness enforcement."""

from __future__ import annotations

from datetime import datetime, timezone
from fastapi import HTTPException, status

from app.adapters.demo.news import DemoNewsProvider
from app.adapters.free_news import compute_freshness
from app.adapters.normalized import NewsRecord
from app.adapters.registry import get_registry
from app.schemas.news import NewsArticleResponse, NewsListResponse


def list_news(
    q: str = "",
    category: str = "",
    symbol: str = "",
    country: str = "",
    freshness: str = "",
    max_age_hours: float | None = None,
    page: int = 1,
    page_size: int = 20,
) -> NewsListResponse:
    registry = get_registry()
    gateway = registry.gateway
    demo_provider = DemoNewsProvider()

    news_result = gateway.fetch(
        provider_name=registry.news_provider.name,
        retrieve=registry.news_provider.list_articles,
        persist=lambda repo, items: repo.save_news(items),
        load_cache=lambda repo: repo.load_news(),
        fallback=demo_provider.list_articles,
    )
    raw_articles: list[NewsRecord] = news_result.items
    now = datetime.now(timezone.utc)

    # 1. Deduplication using content hash / normalized title & dynamically re-evaluate freshness against current UTC clock
    seen_hashes = set()
    deduped: list[NewsRecord] = []
    for item in raw_articles:
        h = item.content_hash or item.compute_hash()
        item.content_hash = h
        if h not in seen_hashes:
            seen_hashes.add(h)
            # Dynamically recalculate freshness against current UTC clock
            f_state, age_h = compute_freshness(item.published_at, now)
            item.freshness = f_state
            item.age_hours = age_h
            deduped.append(item)

    # 2. Sort strictly newest-first (published_at DESC)
    deduped.sort(key=lambda a: a.published_at, reverse=True)

    # 3. Apply Filters
    filtered = deduped

    # Default Freshness Policy:
    # If no explicit historical query / filter is passed, the primary Latest News feed shows CURRENT & RECENT (<= 48-72h)
    if max_age_hours is not None:
        filtered = [a for a in filtered if (a.age_hours is not None and a.age_hours <= max_age_hours)]
    elif freshness.strip():
        f_target = freshness.strip().upper()
        if f_target != "ALL":
            filtered = [a for a in filtered if a.freshness == f_target]
    elif not q.strip() and not symbol.strip() and news_result.data_status == "live":
        # Default live feed: exclude STALE (> 7 days) and prioritize CURRENT + RECENT
        live_current = [a for a in filtered if a.freshness in {"CURRENT", "RECENT"}]
        filtered = live_current if live_current else [a for a in filtered if a.freshness != "STALE"]

    if q.strip():
        query_lower = q.strip().lower()
        filtered = [
            a for a in filtered
            if query_lower in a.headline.lower()
            or query_lower in a.summary.lower()
            or any(query_lower in ent.lower() for ent in a.related_entities)
            or any(query_lower in sec.lower() for sec in a.related_sectors)
        ]

    if category.strip():
        cat_lower = category.strip().lower()
        filtered = [a for a in filtered if a.category.lower() == cat_lower]

    if symbol.strip():
        sym_upper = symbol.strip().upper()
        filtered = [
            a for a in filtered
            if any(sym_upper in ent.upper() for ent in a.related_entities)
        ]

    if country.strip():
        c_lower = country.strip().lower()
        filtered = [
            a for a in filtered
            if any(c_lower in c.lower() for c in a.countries)
        ]

    total = len(filtered)
    start_idx = max(0, (page - 1) * page_size)
    end_idx = start_idx + page_size
    paged = filtered[start_idx:end_idx]

    articles = [
        NewsArticleResponse(
            id=a.id or a.content_hash,
            headline=a.headline,
            summary=a.summary,
            source=a.source,
            source_url=a.source_url,
            published_at=a.published_at,
            category=a.category,
            related_entities=a.related_entities,
            related_sectors=a.related_sectors,
            countries=a.countries,
            language=a.language,
            author=a.author,
            freshness=a.freshness,
            age_hours=a.age_hours,
            provider=a.provider,
            data_status=a.data_status,
            content_hash=a.content_hash,
            retrieved_at=a.retrieved_at or now,
        )
        for a in paged
    ]

    return NewsListResponse(
        articles=articles,
        total=total,
        page=page,
        page_size=page_size,
        data_status=news_result.data_status,
        retrieved_at=now,
    )


def get_news_article(article_id: str) -> NewsArticleResponse:
    list_resp = list_news(page=1, page_size=100, freshness="ALL")
    target = article_id.strip().lower()

    for a in list_resp.articles:
        if (a.id and a.id.lower() == target) or (a.content_hash and a.content_hash.lower() == target):
            return a

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"News article '{article_id}' not found.",
    )
