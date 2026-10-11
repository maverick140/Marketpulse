"""System status endpoint."""

from fastapi import APIRouter

from app.schemas.system import ProviderListResponse, SystemStatusResponse
from app.services.system import get_provider_statuses, get_system_status

router = APIRouter(tags=["system"])


@router.get("/status", response_model=SystemStatusResponse)
def system_status() -> SystemStatusResponse:
    return get_system_status()


@router.get("/providers", response_model=ProviderListResponse)
def system_providers() -> ProviderListResponse:
    return get_provider_statuses()
