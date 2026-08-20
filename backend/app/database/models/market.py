"""Market-related domain models."""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base
from app.database.models.mixins import ExternalDataMixin, TimestampMixin


class Company(TimestampMixin, Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sector: Mapped[str | None] = mapped_column(String(128), nullable=True)
    country: Mapped[str | None] = mapped_column(String(128), nullable=True)


class Security(TimestampMixin, Base):
    __tablename__ = "securities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sector: Mapped[str | None] = mapped_column(String(128), nullable=True)
    company_id: Mapped[int | None] = mapped_column(
        ForeignKey("companies.id"), nullable=True
    )


class MarketPrice(TimestampMixin, ExternalDataMixin, Base):
    __tablename__ = "market_prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)
    change: Mapped[float | None] = mapped_column(Numeric(18, 6), nullable=True)
    change_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    volume: Mapped[int | None] = mapped_column(Integer, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class Index(TimestampMixin, ExternalDataMixin, Base):
    """Market index (named Index per the project specification)."""

    __tablename__ = "market_indices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)
    change: Mapped[float | None] = mapped_column(Numeric(18, 6), nullable=True)
    change_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class Watchlist(TimestampMixin, Base):
    __tablename__ = "watchlist_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    label: Mapped[str | None] = mapped_column(String(255), nullable=True)
