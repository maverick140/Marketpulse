"""Unit tests for News Freshness, Timestamp Normalization & Current-Data Handling."""

from datetime import datetime, timedelta, timezone
from app.adapters.free_geopolitical import FreeGeopoliticalProvider, compute_geo_freshness
from app.adapters.free_news import FreeNewsProvider, compute_freshness
from app.adapters.normalized import NewsRecord
from app.schemas.ai import AIResearchRequest
from app.services.ai import synthesize_research
from app.services.geopolitics import list_geopolitical_events
from app.services.news import list_news


def test_freshness_classification_boundaries() -> None:
    now = datetime(2026, 8, 20, 12, 0, 0, tzinfo=timezone.utc)

    # 1. Fresh article (2 hours old) -> CURRENT
    dt_2h = now - timedelta(hours=2)
    f_state, age_h = compute_freshness(dt_2h, now)
    assert f_state == "CURRENT"
    assert age_h == 2.0

    # 2. 24-hour-old article -> CURRENT
    dt_24h = now - timedelta(hours=24)
    f_state, age_h = compute_freshness(dt_24h, now)
    assert f_state == "CURRENT"
    assert age_h == 24.0

    # 3. 48-hour-old article -> RECENT
    dt_48h = now - timedelta(hours=48)
    f_state, age_h = compute_freshness(dt_48h, now)
    assert f_state == "RECENT"
    assert age_h == 48.0

    # 4. 3-day-old article -> BACKGROUND
    dt_3d = now - timedelta(days=3)
    f_state, age_h = compute_freshness(dt_3d, now)
    assert f_state == "BACKGROUND"
    assert age_h == 72.0

    # 5. 30-day-old article -> STALE
    dt_30d = now - timedelta(days=30)
    f_state, age_h = compute_freshness(dt_30d, now)
    assert f_state == "STALE"
    assert age_h == 720.0

    # 6. January article evaluated in August -> STALE
    dt_jan = datetime(2026, 1, 15, 10, 0, 0, tzinfo=timezone.utc)
    f_state, age_h = compute_freshness(dt_jan, now)
    assert f_state == "STALE"
    assert age_h > 4000.0


def test_naive_timestamp_normalization() -> None:
    now = datetime(2026, 8, 20, 12, 0, 0, tzinfo=timezone.utc)
    naive_dt = datetime(2026, 8, 20, 10, 0, 0)  # Naive without tzinfo

    f_state, age_h = compute_freshness(naive_dt, now)
    assert f_state == "CURRENT"
    assert age_h == 2.0


def test_articles_sorted_newest_first() -> None:
    res = list_news()
    assert res.total > 0
    assert len(res.articles) > 0

    # Verify sorting: every article must be <= preceding article timestamp
    for i in range(len(res.articles) - 1):
        assert res.articles[i].published_at >= res.articles[i + 1].published_at


def test_deduplication_removes_duplicate_headlines() -> None:
    res = list_news()
    seen = set()
    for a in res.articles:
        norm = f"{a.headline.strip().lower()}|{a.source.strip().lower()}"
        assert norm not in seen, f"Duplicate article found: {norm}"
        seen.add(norm)


def test_ai_analyst_today_query_uses_fresh_news() -> None:
    res = synthesize_research(AIResearchRequest(query="What are today's major market headlines?"))
    assert res.summary
    assert len(res.evidence) > 0
    assert res.news_factors is not None


def test_geopolitical_freshness_and_sorting() -> None:
    res = list_geopolitical_events()
    assert res.total > 0
    # Verify sorting newest first
    for i in range(len(res.events) - 1):
        assert res.events[i].event_date >= res.events[i + 1].event_date

    # Verify freshness metadata is present
    for e in res.events:
        assert e.freshness in {"CURRENT", "RECENT", "BACKGROUND", "STALE"}
        assert e.age_hours is not None
