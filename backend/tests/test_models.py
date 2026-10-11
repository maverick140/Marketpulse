"""Phase 2 database model tests."""

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.database import Base, engine as app_engine, init_db
from app.database.models import (
    AIInsight,
    Announcement,
    AuditLog,
    Company,
    Country,
    DataSource,
    GeopoliticalEvent,
    Index,
    MacroIndicator,
    MarketPrice,
    NewsArticle,
    SavedResearch,
    Security,
    SentimentResult,
    Watchlist,
)


EXPECTED_TABLES = {
    "companies",
    "securities",
    "market_prices",
    "market_indices",
    "watchlist_items",
    "news_articles",
    "sentiment_results",
    "countries",
    "geopolitical_events",
    "announcements",
    "macro_indicators",
    "ai_insights",
    "data_sources",
    "audit_logs",
    "saved_research",
}


def test_metadata_includes_domain_tables() -> None:
    assert EXPECTED_TABLES.issubset(set(Base.metadata.tables))


def test_init_db_creates_tables() -> None:
    init_db()
    inspector = inspect(app_engine)
    created = set(inspector.get_table_names())
    assert EXPECTED_TABLES.issubset(created)


def test_models_can_be_persisted() -> None:
    memory = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(memory)
    session_factory = sessionmaker(bind=memory)
    session: Session = session_factory()
    try:
        company = Company(name="Demo Company", sector="Energy", country="India")
        session.add(company)
        session.flush()
        session.add(Security(symbol="RELIANCE", name="Reliance (demo)", company_id=company.id))
        session.add(
            MarketPrice(
                symbol="RELIANCE",
                name="Reliance (demo)",
                price=100.0,
                change=1.0,
                change_percent=1.0,
                volume=1000,
                timestamp=company.created_at,
                provider="demo",
                data_status="demo",
            )
        )
        session.add(
            Index(
                symbol="NIFTY 50",
                name="NIFTY 50",
                value=23000.0,
                timestamp=company.created_at,
                provider="demo",
                data_status="demo",
            )
        )
        session.add(Watchlist(symbol="RELIANCE"))
        article = NewsArticle(
            headline="Demo headline",
            summary="Demo summary",
            provider="demo",
            data_status="demo",
            related_entities=["RELIANCE"],
        )
        session.add(article)
        session.flush()
        session.add(
            SentimentResult(
                news_article_id=article.id,
                label="neutral",
                score=0.0,
                provider="demo",
                data_status="demo",
            )
        )
        session.add(Country(name="India", region="South Asia", iso_code="IN"))
        session.add(
            GeopoliticalEvent(
                title="Demo event",
                region="South Asia",
                country="India",
                category="Trade",
                provider="demo",
                data_status="demo",
                related_sectors=["Energy"],
            )
        )
        session.add(
            Announcement(
                title="Demo announcement",
                category="Corporate",
                provider="demo",
                data_status="demo",
                related_sectors=["Technology"],
            )
        )
        session.add(
            MacroIndicator(
                indicator="Inflation",
                value=4.8,
                unit="percent",
                provider="demo",
                data_status="demo",
            )
        )
        session.add(
            AIInsight(
                insight="Demo observation only.",
                explanation="Educational placeholder.",
                provider="demo",
                data_status="demo",
                evidence=[],
                risk_flags=[],
                sources=[],
            )
        )
        session.add(DataSource(name="demo-market", source_type="market", status="demo"))
        session.add(AuditLog(action="create", entity_type="company", details="test"))
        session.add(SavedResearch(title="Note", content="# demo"))
        session.commit()
        assert session.query(Company).count() == 1
        assert session.query(Security).count() == 1
        assert session.query(MarketPrice).count() == 1
        assert session.query(Index).count() == 1
    finally:
        session.close()
        memory.dispose()
