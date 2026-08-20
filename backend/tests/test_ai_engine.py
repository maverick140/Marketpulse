"""Unit tests for AI Contextual Intelligence Synthesizer."""

from app.schemas.ai import AIResearchRequest
from app.services.ai import get_ai_insights, synthesize_research


def test_synthesize_research_general_query() -> None:
    req = AIResearchRequest(query="Provide a comprehensive outlook on the Indian market macro setup.")
    resp = synthesize_research(req)
    assert resp.query == req.query
    assert "macro" in resp.summary.lower() or "market" in resp.summary.lower()
    assert len(resp.macro_factors) >= 2
    assert len(resp.evidence) >= 2
    assert "Educational and research demonstration only" in resp.disclaimer
    assert "not investment advice" in resp.disclaimer.lower()


def test_synthesize_research_sector_focus() -> None:
    req = AIResearchRequest(query="Analyze Technology sector outlook and exports.", sector="Technology")
    resp = synthesize_research(req)
    assert "Technology" in resp.summary or "Technology" in resp.market_context
    assert len(resp.risk_factors) >= 1
    assert len(resp.uncertainties) >= 1


def test_get_ai_insights_bundle() -> None:
    bundle = get_ai_insights()
    assert bundle.total >= 3
    assert len(bundle.insights) >= 3
    for ins in bundle.insights:
        assert ins.summary
        assert ins.evidence
        assert ins.disclaimer


def test_nifty_sub_intents_produce_distinct_analyses() -> None:
    moving = synthesize_research(AIResearchRequest(query="Why is NIFTY moving today?"))
    falling = synthesize_research(AIResearchRequest(query="What could cause NIFTY to fall?"))
    bullish = synthesize_research(AIResearchRequest(query="Is NIFTY currently bullish or bearish?"))
    support = synthesize_research(AIResearchRequest(query="What factors could support NIFTY over the next few sessions?"))

    assert moving.summary != falling.summary
    assert falling.summary != bullish.summary
    assert bullish.summary != support.summary

    assert "downside catalysts" in falling.summary.lower() or "decline" in falling.summary.lower()
    assert "rsi" in bullish.summary.lower() or "sma" in bullish.summary.lower() or "trend stance" in bullish.summary.lower()
    assert "support" in support.summary.lower() or "sip inflows" in support.summary.lower()


def test_reliance_sub_intents_produce_distinct_analyses() -> None:
    overview = synthesize_research(AIResearchRequest(query="Analyze Reliance Industries."))
    risks = synthesize_research(AIResearchRequest(query="What are the risks for Reliance right now?"))
    catalysts = synthesize_research(AIResearchRequest(query="What factors could drive Reliance higher?"))
    crude_impact = synthesize_research(AIResearchRequest(query="How could crude oil prices affect Reliance?"))

    assert overview.summary != risks.summary
    assert risks.summary != catalysts.summary
    assert catalysts.summary != crude_impact.summary

    assert "vulnerabilities" in risks.summary.lower() or "downside" in risks.summary.lower()
    assert "upside catalysts" in catalysts.summary.lower() or "growth" in catalysts.summary.lower()
    assert "refining margins" in crude_impact.summary.lower() or "jamnagar" in crude_impact.summary.lower()


def test_crude_cross_impact_sub_intents() -> None:
    crude_general = synthesize_research(AIResearchRequest(query="What is happening with crude oil?"))
    crude_india = synthesize_research(AIResearchRequest(query="Why does crude oil matter to India?"))
    crude_rupee = synthesize_research(AIResearchRequest(query="How could higher crude oil prices affect the Indian rupee?"))
    crude_equities = synthesize_research(AIResearchRequest(query="How could higher crude oil prices affect Indian equities?"))

    assert crude_general.summary != crude_rupee.summary
    assert crude_rupee.summary != crude_equities.summary

    assert "import bill" in crude_rupee.summary.lower() or "dollar demand" in crude_rupee.summary.lower()
    assert "sectoral channels" in crude_equities.summary.lower() or "omcs" in crude_equities.summary.lower()
