"""Macroeconomic data service layer."""

from __future__ import annotations

from datetime import datetime, timezone
from fastapi import HTTPException, status

from app.adapters.demo.macro import DemoMacroProvider
from app.adapters.normalized import MacroHistoryPoint, MacroRecord
from app.adapters.registry import get_registry
from app.schemas.macro import (
    MacroDetailResponse,
    MacroHistoryPoint as MacroHistoryPointSchema,
    MacroIndicatorResponse,
    MacroListResponse,
)


def list_macro_indicators() -> MacroListResponse:
    registry = get_registry()
    gateway = registry.gateway
    demo_provider = DemoMacroProvider()

    macro_result = gateway.fetch(
        provider_name=registry.macro_provider.name,
        retrieve=registry.macro_provider.list_indicators,
        persist=lambda repo, items: repo.save_macro(items),
        load_cache=lambda repo: repo.load_macro(),
        fallback=demo_provider.list_indicators,
    )
    records: list[MacroRecord] = macro_result.items

    indicators = [_to_indicator_response(r) for r in records]

    return MacroListResponse(
        indicators=indicators,
        count=len(indicators),
        data_status=macro_result.data_status,
        retrieved_at=datetime.now(timezone.utc),
    )


def get_macro_detail(indicator_name: str) -> MacroDetailResponse:
    target = indicator_name.strip().lower()
    alias_map = {
        "gdp growth": "Real GDP Growth",
        "real gdp": "Real GDP Growth",
        "gdp": "Real GDP Growth",
        "quarterly real gdp growth": "Real GDP Growth",
        "gdp growth rate": "Real GDP Growth",
        "inflation": "CPI Inflation",
        "cpi": "CPI Inflation",
        "cpi inflation": "CPI Inflation",
        "cpi combined inflation": "CPI Inflation",
        "cpi year-on-year inflation": "CPI Inflation",
        "repo rate": "Policy Repo Rate",
        "policy repo rate": "Policy Repo Rate",
        "interest rate": "Policy Repo Rate",
        "rbi repo rate": "Policy Repo Rate",
        "oil": "Brent Crude Oil",
        "brent": "Brent Crude Oil",
        "brent crude oil": "Brent Crude Oil",
        "gold": "Gold",
        "currency": "USD / INR",
        "usd / inr": "USD / INR",
        "usdinr": "USD / INR",
    }
    normalized_target = alias_map.get(target, target).lower()
    list_resp = list_macro_indicators()

    current_item: MacroIndicatorResponse | None = None
    for ind in list_resp.indicators:
        ind_low = ind.indicator.strip().lower()
        if ind_low == target or ind_low == normalized_target:
            current_item = ind
            break

    if not current_item:
        for ind in list_resp.indicators:
            ind_low = ind.indicator.strip().lower()
            if target in ind_low or normalized_target in ind_low or ind_low in normalized_target:
                current_item = ind
                break

    if not current_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Macroeconomic indicator '{indicator_name}' not found.",
        )

    registry = get_registry()
    demo_provider = DemoMacroProvider()

    history: list[MacroHistoryPoint] = []
    try:
        history = registry.macro_provider.get_indicator_history(current_item.indicator)
    except Exception:
        pass

    if not history:
        history = demo_provider.get_indicator_history(current_item.indicator)

    history_schemas = [
        MacroHistoryPointSchema(
            period=h.period,
            value=h.value,
            date=h.date,
        )
        for h in history
    ]

    return MacroDetailResponse(
        indicator=current_item.indicator,
        current=current_item,
        history=history_schemas,
        data_status=list_resp.data_status,
    )


def _to_indicator_response(r: MacroRecord) -> MacroIndicatorResponse:
    return MacroIndicatorResponse(
        indicator=r.indicator,
        value=r.value,
        unit=r.unit,
        period=r.period,
        previous_value=r.previous_value,
        change=r.change,
        source=r.source,
        provider=r.provider,
        data_status=r.data_status,
        retrieved_at=r.retrieved_at,
    )
