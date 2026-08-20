"""Environment-based application settings.

No API keys are required. Optional secrets must never be logged or returned
by the API.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

BACKEND_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(BACKEND_ROOT / ".env")

SECRET_ENV_NAMES = frozenset(
    {
        "API_KEY",
        "SECRET",
        "PASSWORD",
        "TOKEN",
        "OPENAI",
        "NEWSAPI",
    }
)


def _env(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return value.strip()


def _normalize_database_url(url: str) -> str:
    """Resolve relative SQLite paths against the backend directory."""
    prefix = "sqlite:///./"
    if url.startswith(prefix):
        relative = url[len(prefix) :]
        absolute = (BACKEND_ROOT / relative).resolve()
        return f"sqlite:///{absolute.as_posix()}"
    return url


def _parse_origins(raw: str) -> list[str]:
    origins = [item.strip() for item in raw.split(",") if item.strip()]
    default_origins = [
        "https://market-pulses.netlify.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    for o in default_origins:
        if o not in origins:
            origins.append(o)
    return origins


class Settings(BaseModel):
    app_name: str = Field(default="MarketPulse AI")
    app_env: str = Field(default="development")
    app_version: str = Field(default="1.0.0")
    data_mode: str = Field(default="demo")
    database_url: str = Field(default="sqlite:///./marketpulse.db")
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "https://market-pulses.netlify.app",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )
    log_level: str = Field(default="INFO")
    market_provider: str = Field(default="demo")
    news_provider: str = Field(default="demo")
    macro_provider: str = Field(default="demo")
    geopolitical_provider: str = Field(default="demo")
    announcement_provider: str = Field(default="demo")
    market_cache_ttl_seconds: int = Field(default=60)
    macro_cache_ttl_seconds: int = Field(default=900)
    news_cache_ttl_seconds: int = Field(default=1800)

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() in {"production", "prod"}


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=_env("APP_NAME", "MarketPulse AI"),
        app_env=_env("APP_ENV", "development"),
        app_version=_env("APP_VERSION", "1.0.0"),
        data_mode=_env("DATA_MODE", "demo"),
        database_url=_normalize_database_url(
            _env("DATABASE_URL", "sqlite:///./marketpulse.db")
        ),
        cors_origins=_parse_origins(
            _env(
                "CORS_ORIGINS",
                "https://market-pulses.netlify.app,http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000",
            )
        ),
        log_level=_env("LOG_LEVEL", "INFO"),
        market_provider=_env("MARKET_PROVIDER", "demo"),
        news_provider=_env("NEWS_PROVIDER", "demo"),
        macro_provider=_env("MACRO_PROVIDER", "demo"),
        geopolitical_provider=_env("GEOPOLITICAL_PROVIDER", "demo"),
        announcement_provider=_env("ANNOUNCEMENT_PROVIDER", "demo"),
        market_cache_ttl_seconds=int(_env("MARKET_CACHE_TTL_SECONDS", "60")),
        macro_cache_ttl_seconds=int(_env("MACRO_CACHE_TTL_SECONDS", "900")),
        news_cache_ttl_seconds=int(_env("NEWS_CACHE_TTL_SECONDS", "1800")),
    )
