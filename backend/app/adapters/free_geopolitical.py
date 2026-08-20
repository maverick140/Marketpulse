"""Free geopolitical risk intelligence provider using real-time public feeds with freshness controls."""

from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import html
import re
import xml.etree.ElementTree as ET
import httpx

from app.adapters.exceptions import ProviderError
from app.adapters.interfaces import GeopoliticalProvider
from app.adapters.normalized import GeopoliticalRecord
from app.core.logging_config import get_logger

logger = get_logger("free_geopolitical")


def compute_geo_freshness(event_date: datetime, now: datetime | None = None) -> tuple[str, float]:
    """Calculate geopolitical event age in hours and freshness state."""
    if now is None:
        now = datetime.now(timezone.utc)
    if event_date.tzinfo is None:
        event_date = event_date.replace(tzinfo=timezone.utc)
    else:
        event_date = event_date.astimezone(timezone.utc)

    diff_seconds = max(0.0, (now - event_date).total_seconds())
    age_hours = round(diff_seconds / 3600.0, 1)

    if age_hours <= 48.0:
        freshness = "CURRENT"
    elif age_hours <= 120.0:
        freshness = "RECENT"
    elif age_hours <= 336.0:
        freshness = "BACKGROUND"
    else:
        freshness = "STALE"

    return freshness, age_hours


class FreeGeopoliticalProvider(GeopoliticalProvider):
    """Free geopolitical intelligence provider parsing current international risk feeds."""

    name = "free"
    mode = "live"

    def __init__(self, timeout_seconds: float = 8.0) -> None:
        super().__init__()
        self.timeout = timeout_seconds

    def capabilities(self) -> list[str]:
        return ["events", "search"]

    def list_events(self) -> list[GeopoliticalRecord]:
        """Fetch and structure real-time geopolitical and macroeconomic risk events from public RSS."""
        rss_url = "https://news.google.com/rss/search?q=when:3d+geopolitics+OR+sanctions+OR+tariffs+OR+conflict+OR+diplomacy+OR+oil+trade&hl=en-US&gl=US&ceid=US:en"
        events: list[GeopoliticalRecord] = []
        now = datetime.now(timezone.utc)
        seen_hashes: set[str] = set()

        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                resp = client.get(
                    rss_url,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                )
                if resp.status_code == 200:
                    root = ET.fromstring(resp.content)
                    items = root.findall(".//item")
                    for item in items:
                        title_elem = item.find("title")
                        desc_elem = item.find("description")
                        source_elem = item.find("source")
                        pub_elem = item.find("pubDate")

                        title = html.unescape(title_elem.text) if title_elem is not None and title_elem.text else ""
                        desc = html.unescape(desc_elem.text) if desc_elem is not None and desc_elem.text else title
                        desc = re.sub(r"<[^>]+>", "", desc).strip()
                        source_name = source_elem.text if source_elem is not None and source_elem.text else "Global News Wire"

                        if not title:
                            continue

                        # Parse real publication timestamp from RSS
                        event_date = now
                        if pub_elem is not None and pub_elem.text:
                            try:
                                parsed_dt = parsedate_to_datetime(pub_elem.text)
                                if parsed_dt.tzinfo is None:
                                    event_date = parsed_dt.replace(tzinfo=timezone.utc)
                                else:
                                    event_date = parsed_dt.astimezone(timezone.utc)
                            except Exception:
                                event_date = now

                        freshness, age_hours = compute_geo_freshness(event_date, now)

                        norm_key = f"{title.strip().lower()}|{source_name.strip().lower()}"
                        raw_hash = hashlib.sha256(norm_key.encode("utf-8")).hexdigest()

                        if raw_hash in seen_hashes:
                            continue
                        seen_hashes.add(raw_hash)

                        # Determine severity, category, region, and impacts
                        severity_score, relevance_score = self._calculate_scores(title, desc)
                        category = self._classify_category(title, desc)
                        region, country = self._classify_region_and_country(title, desc)
                        sectors, assets = self._map_impact(title, desc)

                        events.append(
                            GeopoliticalRecord(
                                id=f"geo-{raw_hash[:8]}",
                                title=title,
                                description=desc or title,
                                region=region,
                                country=country,
                                category=category,
                                severity=int(severity_score),
                                event_date=event_date,
                                market_relevance=int(relevance_score),
                                related_sectors=sectors,
                                affected_assets=assets,
                                freshness=freshness,
                                age_hours=age_hours,
                                provider=self.name,
                                data_status="live",
                                source=source_name,
                                retrieved_at=now,
                            )
                        )

            if not events:
                raise ProviderError("Zero geopolitical events parsed from real-time feed")

            # Sort strictly newest first
            events.sort(key=lambda e: e.event_date, reverse=True)

            self._tracker.mark_available(self.capabilities())
            return events
        except Exception as exc:
            msg = f"FreeGeopoliticalProvider failed: {exc.__class__.__name__}"
            self._tracker.mark_error(msg)
            raise ProviderError(msg) from exc

    def _calculate_scores(self, title: str, desc: str) -> tuple[int, int]:
        """Derive transparent severity (0-100) and market relevance (0-100)."""
        text = f"{title} {desc}".lower()

        # Severity
        if any(w in text for w in ["war", "strike", "attack", "missile", "blockade", "invasion", "kill"]):
            severity = 90
        elif any(w in text for w in ["sanction", "embargo", "curb", "export ban", "blacklist", "penalty"]):
            severity = 75
        elif any(w in text for w in ["tariff", "duty", "trade war", "restriction"]):
            severity = 65
        elif any(w in text for w in ["tension", "dispute", "standoff", "alert", "probe", "threat"]):
            severity = 50
        elif any(w in text for w in ["talks", "summit", "dialogue", "accord", "treaty", "cooperation", "deal"]):
            severity = 30
        else:
            severity = 45

        # Market Relevance
        if any(w in text for w in ["oil", "gas", "energy", "shipping", "red sea", "strait", "hormuz", "semiconductor", "chip", "rate", "inflation", "dollar"]):
            relevance = min(100, severity + 15)
        elif any(w in text for w in ["trade", "tariff", "export", "import", "supply chain"]):
            relevance = severity
        else:
            relevance = max(20, severity - 15)

        return severity, relevance

    def _classify_category(self, title: str, desc: str) -> str:
        text = f"{title} {desc}".lower()
        if any(w in text for w in ["war", "military", "conflict", "clash", "strike", "missile", "defense", "drone", "kill"]):
            return "Armed Conflict & Security"
        if any(w in text for w in ["tariff", "trade war", "protectionism", "duty", "wto", "customs", "trade deal"]):
            return "Tariffs & Trade Disputes"
        if any(w in text for w in ["sanction", "embargo", "blacklist", "asset freeze", "swift", "penalty"]):
            return "Sanctions & Restrictions"
        if any(w in text for w in ["oil", "gas", "pipeline", "opec", "energy", "crude", "red sea", "strait", "hormuz"]):
            return "Energy & Maritime Security"
        if any(w in text for w in ["tech", "chip", "semiconductor", "ai", "telecom", "rare earth"]):
            return "Technology & Export Controls"
        return "Diplomatic & Strategic Policy"

    def _classify_region_and_country(self, title: str, desc: str) -> tuple[str, str]:
        text = f"{title} {desc}".lower()
        if any(w in text for w in ["india", "delhi", "mumbai", "pakistan", "bangladesh", "sri lanka", "south asia"]):
            return "South Asia", "India" if any(w in text for w in ["india", "delhi", "mumbai"]) else "South Asia"
        if any(w in text for w in ["middle east", "israel", "iran", "saudi", "uae", "gaza", "red sea", "yemen", "qatar", "gulf", "hormuz", "dubai"]):
            return "Middle East", "Middle East"
        if any(w in text for w in ["europe", "ukraine", "russia", "eu", "nato", "germany", "france", "uk", "britain", "moscow", "kyiv", "brussels", "danube", "romania"]):
            return "Europe", "Europe"
        if any(w in text for w in ["china", "taiwan", "japan", "korea", "beijing", "tokyo", "seoul", "east asia"]):
            return "East Asia", "East Asia"
        if any(w in text for w in ["us", "usa", "america", "washington", "biden", "trump", "canada", "carney"]):
            return "North America", "United States"
        return "Global", "International"

    def _map_impact(self, title: str, desc: str) -> tuple[list[str], list[str]]:
        text = f"{title} {desc}".lower()
        sectors: list[str] = []
        assets: list[str] = []

        if any(w in text for w in ["oil", "gas", "energy", "fuel", "crude", "opec", "hormuz"]):
            sectors.append("Energy")
            assets.extend(["Brent Crude", "RELIANCE", "OMCs"])
        if any(w in text for w in ["shipping", "freight", "red sea", "container", "port", "maritime"]):
            sectors.append("Logistics & Shipping")
            assets.extend(["Global Freight Rates", "Ports"])
        if any(w in text for w in ["tech", "chip", "semiconductor", "rare earth", "software"]):
            sectors.append("Technology")
            assets.extend(["TCS", "INFY", "Semiconductor Index"])
        if any(w in text for w in ["defense", "military", "missile", "weapon", "arms"]):
            sectors.append("Defense")
            assets.extend(["Defense Equities", "Government Bonds"])
        if any(w in text for w in ["bank", "dollar", "forex", "currency", "swift", "finance", "penalty"]):
            sectors.append("Financials")
            assets.extend(["USD/INR", "Bond Yields"])
        if not sectors:
            sectors = ["General Equities", "Commodities"]
            assets = ["NIFTY 50", "USD/INR"]

        return sectors, assets
