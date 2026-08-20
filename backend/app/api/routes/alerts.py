"""Alerts and Real-time Monitoring API routes."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.schemas.alerts import AlertItem, AlertListResponse
from app.services.alerts import get_alert, list_alerts

router = APIRouter(tags=["alerts"])


@router.get("", response_model=AlertListResponse)
def get_alerts(
    type: str = Query(default="", description="Alert type filter"),
    severity: str = Query(default="", description="Severity level filter (INFO, WARNING, CRITICAL)"),
    entity: str = Query(default="", description="Entity name or symbol filter"),
) -> AlertListResponse:
    """Retrieve active market, geopolitical, and macroeconomic intelligence alerts."""
    return list_alerts(alert_type=type, severity=severity, entity=entity)


@router.get("/{id}", response_model=AlertItem)
def get_single_alert(id: str) -> AlertItem:
    """Retrieve a single alert by ID."""
    return get_alert(id)
