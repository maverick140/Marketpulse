"""Health endpoint."""

from fastapi import APIRouter

from app.schemas.system import HealthResponse
from app.services.system import get_health

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return get_health()
