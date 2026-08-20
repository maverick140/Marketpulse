"""Macroeconomic data API routes."""

from __future__ import annotations

from fastapi import APIRouter

from app.schemas.macro import MacroDetailResponse, MacroListResponse
from app.services.macro import get_macro_detail, list_macro_indicators

router = APIRouter(tags=["macro"])


@router.get("", response_model=MacroListResponse)
def macro_list() -> MacroListResponse:
    """Retrieve all macroeconomic indicators."""
    return list_macro_indicators()


@router.get("/{indicator}", response_model=MacroDetailResponse)
def macro_detail(indicator: str) -> MacroDetailResponse:
    """Retrieve details and historical data for a specific macroeconomic indicator."""
    return get_macro_detail(indicator)
