"""Alert generation and monitoring service layer."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from fastapi import HTTPException, status

from app.schemas.alerts import AlertItem, AlertListResponse
from app.services.announcements import list_announcements
from app.services.geopolitics import list_geopolitical_events
from app.services.markets import get_market_overview
from app.services.sentiment import get_market_sentiment


def generate_active_alerts() -> list[AlertItem]:
    """Evaluate market, macro, sentiment, and geopolitical rules to generate active alerts."""
    now = datetime.now(timezone.utc)
    alerts: list[AlertItem] = []

    # 1. Market overview rules
    overview = get_market_overview()

    for g in overview.gainers[:2]:
        if g.change_percent and abs(g.change_percent) >= 0.5:
            key = f"market_gain_{g.symbol}_{now.date()}"
            alerts.append(
                AlertItem(
                    id=f"alert-gain-{g.symbol.lower()}",
                    alert_type="PRICE_SPIKE",
                    severity="INFO" if g.change_percent < 1.0 else "WARNING",
                    entity=g.symbol,
                    message=f"{g.symbol} surged {g.change_percent:+.2f}% to ₹{g.price:.2f}",
                    explanation=f"Strong trading volume of {g.volume:,} observed in {g.sector or 'equities'}.",
                    dedup_key=key,
                    timestamp=now,
                    data_status="demo",
                )
            )

    for d in overview.decliners[:2]:
        if d.change_percent and d.change_percent <= -0.35:
            key = f"market_loss_{d.symbol}_{now.date()}"
            alerts.append(
                AlertItem(
                    id=f"alert-loss-{d.symbol.lower()}",
                    alert_type="PRICE_SPIKE",
                    severity="WARNING",
                    entity=d.symbol,
                    message=f"{d.symbol} declined {d.change_percent:+.2f}% to ₹{d.price:.2f}",
                    explanation="Session selling pressure observed with sectoral rotation.",
                    dedup_key=key,
                    timestamp=now,
                    data_status="demo",
                )
            )

    # 2. Geopolitical severity rules
    geo = list_geopolitical_events()
    for ev in geo.events:
        if ev.severity >= 50:
            key = f"geo_{ev.id}_{now.date()}"
            alerts.append(
                AlertItem(
                    id=f"alert-geo-{ev.id}",
                    alert_type="GEOPOLITICAL_RISK",
                    severity="CRITICAL" if ev.severity >= 70 else "WARNING",
                    entity=ev.country or ev.region,
                    message=f"{ev.severity_label} Risk Alert: {ev.title}",
                    explanation=f"Relevance score {ev.market_relevance}/100. Potential impact on sectors: {', '.join(ev.related_sectors)}.",
                    dedup_key=key,
                    timestamp=now,
                    data_status="demo",
                )
            )

    # 3. Macro Announcement rules
    ann = list_announcements(importance="high")
    for a in ann.announcements:
        key = f"ann_{a.id}_{now.date()}"
        alerts.append(
            AlertItem(
                id=f"alert-ann-{a.id}",
                alert_type="MACRO_RELEASE",
                severity="WARNING" if a.importance == "high" else "INFO",
                entity=a.category,
                message=f"High Priority Release: {a.title}",
                explanation=f"Scheduled for {a.date}. Relevant to: {', '.join(a.related_sectors)}.",
                dedup_key=key,
                timestamp=now,
                data_status="demo",
            )
        )

    # 4. Sentiment shift rules
    sent = get_market_sentiment()
    if abs(sent.overall_score) >= 0.15:
        key = f"sentiment_shift_{now.date()}"
        alerts.append(
            AlertItem(
                id="alert-sent-shift",
                alert_type="SENTIMENT_SHIFT",
                severity="INFO",
                entity="Market Sentiment",
                message=f"Headline news sentiment is {sent.overall_label.upper()} (score: {sent.overall_score:+.2f})",
                explanation=f"Derived from {sent.total_articles} financial articles with {sent.confidence * 100:.0f}% confidence.",
                dedup_key=key,
                timestamp=now,
                data_status="demo",
            )
        )

    # Deduplicate by key
    seen = set()
    deduped: list[AlertItem] = []
    for item in alerts:
        if item.dedup_key not in seen:
            seen.add(item.dedup_key)
            deduped.append(item)

    return deduped


def list_alerts(
    alert_type: str = "",
    severity: str = "",
    entity: str = "",
) -> AlertListResponse:
    raw_alerts = generate_active_alerts()
    filtered = raw_alerts

    if alert_type.strip():
        at_upper = alert_type.strip().upper()
        filtered = [a for a in filtered if a.alert_type.upper() == at_upper]

    if severity.strip():
        sev_upper = severity.strip().upper()
        filtered = [a for a in filtered if a.severity.upper() == sev_upper]

    if entity.strip():
        ent_lower = entity.strip().lower()
        filtered = [a for a in filtered if ent_lower in a.entity.lower()]

    critical_count = sum(1 for a in raw_alerts if a.severity == "CRITICAL")
    warning_count = sum(1 for a in raw_alerts if a.severity == "WARNING")
    info_count = sum(1 for a in raw_alerts if a.severity == "INFO")

    return AlertListResponse(
        alerts=filtered,
        total=len(filtered),
        critical_count=critical_count,
        warning_count=warning_count,
        info_count=info_count,
        generated_at=datetime.now(timezone.utc),
    )


def get_alert(alert_id: str) -> AlertItem:
    alerts = generate_active_alerts()
    target = alert_id.strip().lower()

    for a in alerts:
        if a.id.lower() == target:
            return a

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Alert '{alert_id}' not found.",
    )
