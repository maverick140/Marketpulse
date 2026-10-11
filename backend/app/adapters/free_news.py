"""Free live news intelligence provider using public RSS feeds with strict freshness controls."""

from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import html
import re
import xml.etree.ElementTree as ET
import httpx

from app.adapters.exceptions import ProviderError
from app.adapters.interfaces import NewsProvider
from app.adapters.normalized import NewsRecord
from app.core.logging_config import get_logger

logger = get_logger("free_news")


def compute_freshness(published_at: datetime, now: datetime | None = None) -> tuple[str, float]:
    """Calculate age in hours and freshness classification in UTC."""
    if now is None:
        now = datetime.now(timezone.utc)
    if published_at.tzinfo is None:
        published_at = published_at.replace(tzinfo=timezone.utc)
    else:
        published_at = published_at.astimezone(timezone.utc)

    diff_seconds = max(0.0, (now - published_at).total_seconds())
    age_hours = round(diff_seconds / 3600.0, 1)

    if age_hours <= 24.0:
        freshness = "CURRENT"
    elif age_hours <= 48.0:
        freshness = "RECENT"
    elif age_hours <= 168.0:
        freshness = "BACKGROUND"
    else:
        freshness = "STALE"

    return freshness, age_hours


class FreeNewsProvider(NewsProvider):
    """Free news provider parsing real-time public financial and business RSS feeds."""

    name = "free"
    mode = "live"

    def __init__(self, timeout_seconds: float = 6.0) -> None:
        super().__init__()
        self.timeout = timeout_seconds

    def capabilities(self) -> list[str]:
        return ["articles", "search"]

    def list_articles(self) -> list[NewsRecord]:
        """Fetch and parse live financial news articles from current real-time feeds."""
        rss_urls = [
            "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-IN&gl=IN&ceid=IN:en",
            "https://news.google.com/rss/search?q=when:2d+NSE+OR+BSE+OR+Nifty+OR+Sensex+OR+Indian+economy&hl=en-IN&gl=IN&ceid=IN:en",
        ]
        articles: list[NewsRecord] = []
        now = datetime.now(timezone.utc)
        seen_hashes: set[str] = set()

        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                for url in rss_urls:
                    try:
                        resp = client.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                        if resp.status_code == 200:
                            root = ET.fromstring(resp.content)
                            for item in root.findall(".//item"):
                                title_elem = item.find("title")
                                desc_elem = item.find("description")
                                link_elem = item.find("link")
                                pub_elem = item.find("pubDate")
                                source_elem = item.find("source")

                                headline = html.unescape(title_elem.text) if title_elem is not None and title_elem.text else ""
                                summary = html.unescape(desc_elem.text) if desc_elem is not None and desc_elem.text else headline
                                summary = re.sub(r"<[^>]+>", "", summary).strip()
                                link = link_elem.text if link_elem is not None and link_elem.text else None
                                source_name = source_elem.text if source_elem is not None and source_elem.text else "Financial News Wire"

                                if not headline:
                                    continue

                                # Safe UTC timezone-aware date parsing
                                published_at = now
                                if pub_elem is not None and pub_elem.text:
                                    try:
                                        parsed_dt = parsedate_to_datetime(pub_elem.text)
                                        if parsed_dt.tzinfo is None:
                                            published_at = parsed_dt.replace(tzinfo=timezone.utc)
                                        else:
                                            published_at = parsed_dt.astimezone(timezone.utc)
                                    except Exception:
                                        published_at = now

                                freshness, age_hours = compute_freshness(published_at, now)

                                # Determine categories & entities
                                category = self._classify_category(headline, summary)
                                entities = self._extract_entities(headline, summary)
                                sectors = self._extract_sectors(headline, summary)

                                # Deduplicate by canonical headline + source
                                norm_key = f"{headline.strip().lower()}|{source_name.strip().lower()}"
                                raw_hash = hashlib.sha256(norm_key.encode("utf-8")).hexdigest()

                                if raw_hash in seen_hashes:
                                    continue
                                seen_hashes.add(raw_hash)

                                articles.append(
                                    NewsRecord(
                                        id=f"news-{raw_hash[:10]}",
                                        headline=headline,
                                        summary=summary or headline,
                                        source=source_name,
                                        source_url=link,
                                        published_at=published_at,
                                        category=category,
                                        related_entities=entities,
                                        related_sectors=sectors,
                                        countries=["India"],
                                        language="en",
                                        freshness=freshness,
                                        age_hours=age_hours,
                                        provider=self.name,
                                        data_status="live",
                                        content_hash=raw_hash,
                                        retrieved_at=now,
                                    )
                                )
                    except Exception as e:
                        logger.warning("Failed fetching news RSS feed %s: %s", url, e)

            if not articles:
                raise ProviderError("Zero news articles parsed from free live feed")

            # Sort strictly newest first
            articles.sort(key=lambda a: a.published_at, reverse=True)

            self._tracker.mark_available(self.capabilities())
            return articles
        except Exception as exc:
            msg = f"FreeNewsProvider failed: {exc.__class__.__name__}"
            self._tracker.mark_error(msg)
            raise ProviderError(msg) from exc

    def _classify_category(self, headline: str, summary: str) -> str:
        text = f"{headline} {summary}".lower()
        if any(w in text for w in ["ai ", "software", "tech", "cloud", "chip", "semiconductor", "digital"]):
            return "TECHNOLOGY"
        if any(w in text for w in ["crude", "oil", "gold", "metal", "commodity", "opec", "energy"]):
            return "COMMODITIES"
        if any(w in text for w in ["rbi", "inflation", "cpi", "repo rate", "gdp", "fiscal", "deficit", "tax"]):
            return "MACRO"
        if any(w in text for w in ["war", "conflict", "sanction", "tariff", "israel", "iran", "russia", "china"]):
            return "GEOPOLITICS"
        if any(w in text for w in ["sebi", "regulatory", "court", "tribunal", "penalty", "compliance"]):
            return "REGULATORY"
        return "MARKET"

    def _extract_entities(self, headline: str, summary: str) -> list[str]:
        text = f"{headline} {summary}".upper()
        entity_aliases = {
            "RELIANCE": ["RELIANCE", "RIL"],
            "TCS": ["TCS", "TATA CONSULTANCY"],
            "INFY": ["INFY", "INFOSYS"],
            "HDFCBANK": ["HDFC BANK", "HDFCBANK", "HDFC"],
            "ICICIBANK": ["ICICI BANK", "ICICIBANK", "ICICI"],
            "SBIN": ["SBIN", "STATE BANK OF INDIA", "SBI"],
            "ITC": ["ITC ", "ITC LIMITED"],
            "BHARTIARTL": ["BHARTI AIRTEL", "BHARTIARTL", "AIRTEL"],
            "LT": ["LARSEN & TOUBRO", "L&T"],
            "HINDUNILVR": ["HINDUSTAN UNILEVER", "HINDUNILVR", "HUL"],
            "NIFTY": ["NIFTY", "NIFTY 50", "NIFTY50"],
            "SENSEX": ["SENSEX", "BSESN"],
        }
        res: list[str] = []
        for sym, aliases in entity_aliases.items():
            if any(a in text for a in aliases):
                res.append(sym)
        return res

    def _extract_sectors(self, headline: str, summary: str) -> list[str]:
        text = f"{headline} {summary}".lower()
        sectors: list[str] = []
        if any(w in text for w in ["tech", "software", "it "]):
            sectors.append("Technology")
        if any(w in text for w in ["bank", "finance", "lending", "credit"]):
            sectors.append("Financials")
        if any(w in text for w in ["energy", "oil", "refining", "petrol"]):
            sectors.append("Energy")
        if any(w in text for w in ["fmcg", "consumer", "food"]):
            sectors.append("Consumer Goods")
        if any(w in text for w in ["auto", "car", "ev ", "vehicle"]):
            sectors.append("Automobile")
        return sectors or ["General Markets"]
