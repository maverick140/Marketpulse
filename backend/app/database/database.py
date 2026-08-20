"""SQLAlchemy engine, session factory, and initialization."""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings
from app.core.logging_config import get_logger

logger = get_logger("database")

settings = get_settings()

connect_args: dict[str, object] = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Declarative base for future domain models."""


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    except Exception:
        logger.exception("Database session error")
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    try:
        from app.database import models as _models  # noqa: F401

        Base.metadata.create_all(bind=engine)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info(
            "Database initialized (%s tables)",
            len(Base.metadata.tables),
        )
    except Exception:
        logger.exception("Database initialization failed")
        raise


def check_database() -> str:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return "online"
    except Exception:
        logger.exception("Database health check failed")
        return "offline"
