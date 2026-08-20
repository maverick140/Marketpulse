"""Market intelligence and data service layer."""

from __future__ import annotations

from datetime import datetime, timezone
from fastapi import HTTPException, status

from app.adapters.demo.market import DemoMarketProvider
from app.adapters.normalized import MarketIndexRecord, MarketQuote
from app.adapters.registry import get_registry
from app.analytics.technical import compute_technical_indicators
from app.database.repositories import PersistenceRepository
from app.schemas.markets import (
    HistoricalPoint,
    MACDResponse,
    MarketHistoryResponse,
    MarketIndexResponse,
    MarketOverviewResponse,
    MarketQuoteResponse,
    SecuritySearchItem,
    SecuritySearchResponse,
    TechnicalIndicatorsResponse,
)

VALID_TIMEFRAMES = {"1D", "5D", "1M", "3M", "6M", "1Y"}


def get_market_overview() -> MarketOverviewResponse:
    registry = get_registry()
    gateway = registry.gateway
    demo_provider = DemoMarketProvider()

    # Fetch quotes through fallback gateway
    quotes_result = gateway.fetch(
        provider_name=registry.market_provider.name,
        retrieve=registry.market_provider.list_quotes,
        persist=lambda repo, items: repo.save_quotes(items),
        load_cache=lambda repo: repo.load_quotes(),
        fallback=demo_provider.list_quotes,
    )
    quotes: list[MarketQuote] = quotes_result.items

    # Fetch indices through fallback gateway
    indices_result = gateway.fetch(
        provider_name=registry.market_provider.name,
        retrieve=registry.market_provider.list_indices,
        persist=lambda repo, items: repo.save_indices(items),
        load_cache=lambda repo: repo.load_indices(),
        fallback=demo_provider.list_indices,
    )
    indices: list[MarketIndexRecord] = indices_result.items

    # Sort gainers, decliners, most active
    quotes_with_pct = [q for q in quotes if q.change_percent is not None]
    gainers = sorted(quotes_with_pct, key=lambda x: x.change_percent or 0.0, reverse=True)[:5]
    decliners = sorted(quotes_with_pct, key=lambda x: x.change_percent or 0.0)[:5]
    most_active = sorted(quotes, key=lambda x: x.volume or 0, reverse=True)[:5]

    return MarketOverviewResponse(
        indices=[
            MarketIndexResponse(
                symbol=idx.symbol,
                name=idx.name,
                value=idx.value,
                change=idx.change,
                change_percent=idx.change_percent,
                timestamp=idx.timestamp,
                provider=idx.provider,
                data_status=idx.data_status,
                source=idx.source,
            )
            for idx in indices
        ],
        gainers=[_to_quote_response(q) for q in gainers],
        decliners=[_to_quote_response(q) for q in decliners],
        most_active=[_to_quote_response(q) for q in most_active],
        data_status=quotes_result.data_status,
        retrieved_at=datetime.now(timezone.utc),
    )


def search_securities(query: str = "") -> SecuritySearchResponse:
    registry = get_registry()
    q = (query or "").strip()

    # Check if provider has dynamic search implementation
    try:
        provider_results = registry.market_provider.search(q)
        results = [
            SecuritySearchItem(
                symbol=q_item.symbol,
                name=q_item.name,
                sector=q_item.sector,
                price=q_item.price,
                change_percent=q_item.change_percent,
                provider=q_item.provider,
            )
            for q_item in provider_results
        ]
        return SecuritySearchResponse(
            query=query,
            results=results,
            count=len(results),
        )
    except Exception:
        pass

    # Fallback to local catalog
    overview = get_market_overview()
    all_quotes = overview.gainers + overview.decliners + overview.most_active
    q_up = q.upper()
    filtered = [
        quote for quote in all_quotes
        if q_up in quote.symbol.upper()
        or q_up in quote.name.upper()
        or (quote.sector and q_up in quote.sector.upper())
    ] if q_up else all_quotes

    results = [
        SecuritySearchItem(
            symbol=q_item.symbol,
            name=q_item.name,
            sector=q_item.sector,
            price=q_item.price,
            change_percent=q_item.change_percent,
            provider=q_item.provider,
        )
        for q_item in filtered
    ]

    return SecuritySearchResponse(
        query=query,
        results=results,
        count=len(results),
    )


def get_quote(symbol: str) -> MarketQuoteResponse:
    target = symbol.strip().upper()
    registry = get_registry()
    gateway = registry.gateway
    demo_provider = DemoMarketProvider()

    quotes_result = gateway.fetch(
        provider_name=registry.market_provider.name,
        retrieve=registry.market_provider.list_quotes,
        persist=lambda repo, items: repo.save_quotes(items),
        load_cache=lambda repo: repo.load_quotes(),
        fallback=demo_provider.list_quotes,
    )
    quotes: list[MarketQuote] = quotes_result.items

    for q in quotes:
        if q.symbol.upper() == target:
            return _to_quote_response(q)

    # Check indices if not in equities quotes
    indices_result = gateway.fetch(
        provider_name=registry.market_provider.name,
        retrieve=registry.market_provider.list_indices,
        persist=lambda repo, items: repo.save_indices(items),
        load_cache=lambda repo: repo.load_indices(),
        fallback=demo_provider.list_indices,
    )
    for idx in indices_result.items:
        if idx.symbol.upper() == target or idx.name.upper() == target or target in idx.symbol.upper():
            return MarketQuoteResponse(
                symbol=idx.symbol,
                name=idx.name,
                price=idx.value,
                change=idx.change,
                change_percent=idx.change_percent,
                volume=None,
                timestamp=idx.timestamp,
                provider=idx.provider,
                data_status=idx.data_status,
                source=idx.source,
                source_url=None,
                sector="Headline Index",
                retrieved_at=idx.retrieved_at,
            )

    # Dynamically query provider for non-preloaded stock (e.g. BHEL, NVDA, TMCV.NS, AAPL)
    try:
        dynamic_q = registry.market_provider.get_quote(target)
        if dynamic_q:
            return _to_quote_response(dynamic_q)
    except Exception:
        pass

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Security symbol '{symbol}' not found.",
    )


def get_history(symbol: str, timeframe: str = "1M") -> MarketHistoryResponse:
    tf = (timeframe or "1M").strip().upper()
    if tf not in VALID_TIMEFRAMES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid timeframe '{timeframe}'. Allowed values: {', '.join(sorted(VALID_TIMEFRAMES))}",
        )

    target = symbol.strip().upper()
    registry = get_registry()
    demo_provider = DemoMarketProvider()

    # Try active provider history
    points: list[HistoricalPoint] = []
    data_status = "demo"
    provider_name = "demo"

    try:
        raw_points = registry.market_provider.get_history(target, tf)
        if raw_points:
            points = [
                HistoricalPoint(
                    timestamp=p.timestamp,
                    open=p.open,
                    high=p.high,
                    low=p.low,
                    close=p.close,
                    volume=p.volume,
                )
                for p in raw_points
            ]
            data_status = "live" if registry.market_provider.name != "demo" else "demo"
            provider_name = registry.market_provider.name
    except Exception:
        pass

    if not points:
        demo_points = demo_provider.get_history(target, tf)
        if demo_points:
            points = [
                HistoricalPoint(
                    timestamp=p.timestamp,
                    open=p.open,
                    high=p.high,
                    low=p.low,
                    close=p.close,
                    volume=p.volume,
                )
                for p in demo_points
            ]
            data_status = "demo"
            provider_name = "demo"

    if not points:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Historical data for symbol '{symbol}' not found.",
        )

    return MarketHistoryResponse(
        symbol=target,
        timeframe=tf,
        data_status=data_status,
        provider=provider_name,
        points=points,
    )


def get_indicators(symbol: str, timeframe: str = "1M") -> TechnicalIndicatorsResponse:
    history = get_history(symbol, timeframe)
    closes = [p.close for p in history.points]
    metrics = compute_technical_indicators(closes)

    macd_data = metrics.get("macd", {})
    macd_resp = MACDResponse(
        macd_line=macd_data.get("macd_line"),
        signal_line=macd_data.get("signal_line"),
        histogram=macd_data.get("histogram"),
    )

    return TechnicalIndicatorsResponse(
        symbol=history.symbol,
        timeframe=history.timeframe,
        sma_20=metrics.get("sma_20"),
        sma_50=metrics.get("sma_50"),
        ema_20=metrics.get("ema_20"),
        rsi_14=metrics.get("rsi_14"),
        macd=macd_resp,
        volatility=metrics.get("volatility"),
        max_drawdown=metrics.get("max_drawdown"),
        period_return=metrics.get("period_return"),
        disclaimer=metrics.get("disclaimer", "Educational demonstration only. Not investment advice."),
    )


def _to_quote_response(q: MarketQuote) -> MarketQuoteResponse:
    return MarketQuoteResponse(
        symbol=q.symbol,
        name=q.name,
        price=q.price,
        change=q.change,
        change_percent=q.change_percent,
        volume=q.volume,
        timestamp=q.timestamp,
        provider=q.provider,
        data_status=q.data_status,
        source=q.source,
        source_url=q.source_url,
        sector=q.sector,
        retrieved_at=q.retrieved_at,
    )
