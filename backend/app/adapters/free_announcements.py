"""Free corporate and regulatory announcements provider using live public feeds."""

from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import html
import re
import xml.etree.ElementTree as ET
import httpx

from app.adapters.exceptions import ProviderError
from app.adapters.interfaces import AnnouncementProvider
from app.adapters.normalized import AnnouncementRecord
from app.core.logging_config import get_logger

logger = get_logger("free_announcements")


class FreeAnnouncementProvider(AnnouncementProvider):
    """Free announcement provider fetching corporate and regulatory disclosures."""

    name = "free"
    mode = "live"

    def __init__(self, timeout_seconds: float = 5.0) -> None:
        super().__init__()
        self.timeout = timeout_seconds

    def capabilities(self) -> list[str]:
        return ["announcements"]

    def list_announcements(self) -> list[AnnouncementRecord]:
        """Fetch live announcements and regulatory disclosures."""
        rss_url = "https://news.google.com/rss/search?q=SEBI+RBI+quarterly+earnings+dividend+board+meeting&hl=en-IN&gl=IN&ceid=IN:en"
        announcements: list[AnnouncementRecord] = []
        now = datetime.now(timezone.utc)

        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                resp = client.get(rss_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                if resp.status_code == 200:
                    root = ET.fromstring(resp.content)
                    for item in root.findall(".//item")[:15]:
                        title_elem = item.find("title")
                        desc_elem = item.find("description")
                        link_elem = item.find("link")
                        pub_elem = item.find("pubDate")
                        source_elem = item.find("source")

                        title = html.unescape(title_elem.text) if title_elem is not None and title_elem.text else ""
                        desc = html.unescape(desc_elem.text) if desc_elem is not None and desc_elem.text else title
                        desc = re.sub(r"<[^>]+>", "", desc).strip()
                        link = link_elem.text if link_elem is not None and link_elem.text else None
                        source_name = source_elem.text if source_elem is not None and source_elem.text else "Regulatory Feed"

                        published_at = now
                        if pub_elem is not None and pub_elem.text:
                            try:
                                published_at = parsedate_to_datetime(pub_elem.text)
                            except Exception:
                                published_at = now

                        category = self._classify_category(title, desc)
                        importance = self._classify_importance(title, desc)
                        company = self._extract_company(title, desc)

                        raw_hash = hashlib.sha256(f"{title}-{published_at}".encode("utf-8")).hexdigest()

                        announcements.append(
                            AnnouncementRecord(
                                id=f"ann-{raw_hash[:8]}",
                                title=title,
                                category=category,
                                announcement_type="DISCLOSURE",
                                date=published_at.date(),
                                importance=importance,
                                source=source_name,
                                source_url=link,
                                related_sectors=["Financials", "Markets"],
                                related_entities=[company] if company != "Market Exchange" else ["RBI", "SEBI"],
                                provider=self.name,
                                data_status="live",
                                retrieved_at=now,
                            )
                        )

            if not announcements:
                raise ProviderError("Zero announcements parsed")

            self._tracker.mark_available(self.capabilities())
            return announcements
        except Exception as exc:
            msg = f"FreeAnnouncementProvider failed: {exc.__class__.__name__}"
            self._tracker.mark_error(msg)
            raise ProviderError(msg) from exc

    def _classify_category(self, title: str, desc: str) -> str:
        text = f"{title} {desc}".lower()
        if any(w in text for w in ["dividend", "bonus", "split", "buyback", "agm"]):
            return "CORPORATE_ACTION"
        if any(w in text for w in ["q1", "q2", "q3", "q4", "financial results", "quarterly"]):
            return "FINANCIAL_RESULTS"
        if any(w in text for w in ["sebi", "rbi", "order", "regulation", "penalty", "circular"]):
            return "REGULATORY"
        if any(w in text for w in ["ceo", "cfo", "director", "resignation", "appointment", "board"]):
            return "MANAGEMENT"
        return "GENERAL"

    def _classify_importance(self, title: str, desc: str) -> str:
        text = f"{title} {desc}".lower()
        if any(w in text for w in ["penalty", "ban", "resignation", "investigation", "merger"]):
            return "high"
        if any(w in text for w in ["dividend", "results", "appointment", "acquisition"]):
            return "medium"
        return "low"

    def _extract_company(self, title: str, desc: str) -> str:
        text = f" {title} {desc} ".upper()
        mapping = [
            ("HDFCBANK", ["HDFCBANK", "HDFC BANK"]),
            ("ICICIBANK", ["ICICIBANK", "ICICI BANK"]),
            ("SBIN", ["SBIN", "STATE BANK OF INDIA", "SBI "]),
            ("RELIANCE", ["RELIANCE"]),
            ("TCS", ["TCS", "TATA CONSULTANCY"]),
            ("INFY", ["INFY", "INFOSYS"]),
            ("ITC", [" ITC "]),
            ("BHARTIARTL", ["BHARTIARTL", "BHARTI AIRTEL", "AIRTEL"]),
            ("LT", [" L&T ", "LARSEN & TOUBRO"]),
            ("HINDUNILVR", ["HINDUNILVR", "HINDUSTAN UNILEVER", "HUL"]),
            ("SEBI", ["SEBI"]),
            ("RBI", ["RBI"]),
        ]
        for canonical, aliases in mapping:
            if any(a in text for a in aliases):
                return canonical
        return "Market Exchange"
