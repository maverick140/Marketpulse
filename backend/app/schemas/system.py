"""Health and system status schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
    service: str = Field(examples=["MarketPulse AI"])


class SystemStatusResponse(BaseModel):
    application_status: str = Field(examples=["online"])
    environment: str = Field(examples=["development"])
    data_mode: str = Field(examples=["demo"])
    database_status: str = Field(examples=["online"])
    api_version: str = Field(examples=["0.1.0"])


class ProviderStatusResponse(BaseModel):
    type: str
    provider: str
    status: str
    mode: str
    last_success: datetime | None = None
    last_error: str | None = None


class ProviderListResponse(BaseModel):
    providers: list[ProviderStatusResponse]
