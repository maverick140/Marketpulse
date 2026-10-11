"""Provider status tracking. Never include secrets."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field

ProviderStatusName = Literal["available", "unavailable", "demo", "cached", "error"]


class ProviderStatus(BaseModel):
    provider: str
    type: str
    status: ProviderStatusName
    mode: str
    last_success: datetime | None = None
    last_error: str | None = None
    capabilities: list[str] = Field(default_factory=list)


class StatusTracker:
    def __init__(self, provider: str, provider_type: str, mode: str) -> None:
        self.provider = provider
        self.provider_type = provider_type
        self.mode = mode
        self.status: ProviderStatusName = "unavailable"
        self.last_success: datetime | None = None
        self.last_error: str | None = None
        self.capabilities: list[str] = []

    def snapshot(self) -> ProviderStatus:
        return ProviderStatus(
            provider=self.provider,
            type=self.provider_type,
            status=self.status,
            mode=self.mode,
            last_success=self.last_success,
            last_error=self.last_error,
            capabilities=list(self.capabilities),
        )

    def mark_available(self, capabilities: list[str] | None = None) -> None:
        self.status = "available"
        self.last_success = datetime.now(timezone.utc)
        self.last_error = None
        if capabilities is not None:
            self.capabilities = capabilities

    def mark_error(self, message: str) -> None:
        self.status = "error"
        self.last_error = message

    def mark_unavailable(self, message: str | None = None) -> None:
        self.status = "unavailable"
        if message:
            self.last_error = message
