"""Normalization tests."""

from app.adapters.normalization import (
    normalize_announcement,
    normalize_geopolitical,
    normalize_macro,
    normalize_market_quote,
    normalize_news,
)


def test_normalize_market_quote_maps_alternate_fields() -> None:
    quote = normalize_market_quote(
        {
            "ticker": "tcs",
            "shortName": "TCS demo",
            "last": "100.5",
            "percent_change": "1.2",
            "regularMarketVolume": "10",
            "provider": "demo",
            "data_status": "demo",
        }
    )
    assert quote.symbol == "TCS"
    assert quote.price == 100.5
    assert quote.change_percent == 1.2
    assert quote.volume == 10
    assert quote.data_status == "demo"


def test_normalize_news_maps_title_and_entities() -> None:
    article = normalize_news(
        {
            "title": "Demo: sample",
            "description": "Synthetic summary",
            "publisher": "Demo Research Feed",
            "section": "Markets",
            "tickers": "RELIANCE,TCS",
            "provider": "demo",
        }
    )
    assert article.headline == "Demo: sample"
    assert article.related_entities == ["RELIANCE", "TCS"]
    assert article.data_status == "demo"
    assert article.source_url is None


def test_normalize_macro_and_geo_and_announcements() -> None:
    macro = normalize_macro({"name": "Inflation", "latest": 4.8, "unit": "percent", "as_of": "2024-05"})
    assert macro.indicator == "Inflation"
    geo = normalize_geopolitical(
        {
            "event": "Demo: sample",
            "region": "India",
            "severity": 40,
            "relevance": 50,
            "sectors": ["Energy"],
        }
    )
    assert geo.title == "Demo: sample"
    announcement = normalize_announcement(
        {"headline": "Demo: note", "date": "2024-06-01", "category": "Corporate"}
    )
    assert announcement.title == "Demo: note"
    assert str(announcement.date) == "2024-06-01"
