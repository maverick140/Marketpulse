"""AI Intelligence & Contextual Research API routes."""

from __future__ import annotations

from fastapi import APIRouter

from app.schemas.ai import AIInsightResponse, AIInsightsListResponse, AIResearchRequest
from app.services.ai import get_ai_insights, synthesize_research

router = APIRouter(tags=["ai"])


@router.get("/insights", response_model=AIInsightsListResponse)
def get_insights() -> AIInsightsListResponse:
    """Retrieve pre-compiled AI contextual market and macro intelligence digests."""
    return get_ai_insights()


@router.post("/research", response_model=AIInsightResponse)
def research_query(payload: AIResearchRequest) -> AIInsightResponse:
    """Perform grounded, multi-factor AI research on a financial inquiry."""
    return synthesize_research(payload)
