"""Application logging.

Never log API keys, passwords, secrets, or personal information.
"""

from __future__ import annotations

import logging
import logging.config
from typing import Any

from app.core.config import SECRET_ENV_NAMES, get_settings

LOGGER_NAME = "marketpulse"


class SecretFilter(logging.Filter):
    """Drop log records that appear to mention secret-related names."""

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage().upper()
        return not any(token in message for token in SECRET_ENV_NAMES)


def configure_logging() -> None:
    settings = get_settings()
    level = settings.log_level.upper()
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "secrets": {
                    "()": "app.core.logging_config.SecretFilter",
                }
            },
            "formatters": {
                "standard": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "filters": ["secrets"],
                    "formatter": "standard",
                    "level": level,
                }
            },
            "loggers": {
                LOGGER_NAME: {
                    "handlers": ["console"],
                    "level": level,
                    "propagate": False,
                },
                "sqlalchemy.engine": {
                    "handlers": ["console"],
                    "level": "WARNING",
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": ["console"],
                    "level": level,
                    "propagate": False,
                },
            },
            "root": {
                "handlers": ["console"],
                "level": level,
            },
        }
    )


def get_logger(name: str | None = None) -> logging.Logger:
    if name:
        return logging.getLogger(f"{LOGGER_NAME}.{name}")
    return logging.getLogger(LOGGER_NAME)


def safe_log_extra(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of payload with secret-like keys removed."""
    redacted: dict[str, Any] = {}
    for key, value in payload.items():
        upper = key.upper()
        if any(token in upper for token in SECRET_ENV_NAMES):
            continue
        redacted[key] = value
    return redacted
