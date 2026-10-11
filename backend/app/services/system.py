"""Health and system status services."""

from app.adapters.registry import get_registry
from app.core.config import get_settings
from app.database.database import check_database
from app.schemas.system import (
    HealthResponse,
    ProviderListResponse,
    ProviderStatusResponse,
    SystemStatusResponse,
)


def get_health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", service=settings.app_name)


def get_system_status() -> SystemStatusResponse:
    settings = get_settings()
    return SystemStatusResponse(
        application_status="online",
        environment=settings.app_env,
        data_mode=settings.data_mode,
        database_status=check_database(),
        api_version=settings.app_version,
    )


def get_provider_statuses() -> ProviderListResponse:
    registry = get_registry()
    providers = [
        ProviderStatusResponse(
            type=item.type,
            provider=item.provider,
            status=item.status,
            mode=item.mode,
            last_success=item.last_success,
            last_error=item.last_error,
        )
        for item in registry.statuses()
    ]
    return ProviderListResponse(providers=providers)
