"""Lightweight validation before cache/persistence."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from app.core.logging_config import get_logger

logger = get_logger("validation")

T = TypeVar("T", bound=BaseModel)


def validate_records(records: Iterable[T], factory: Callable[[T], T] | None = None) -> list[T]:
    """Drop invalid items instead of failing the whole request."""
    valid: list[T] = []
    for record in records:
        try:
            item = factory(record) if factory else record
            if hasattr(item, "model_validate"):
                item.model_validate(item.model_dump())
            valid.append(item)
        except (ValidationError, ValueError, TypeError):
            logger.warning("Dropped invalid provider record: %s", type(record).__name__)
    return valid
