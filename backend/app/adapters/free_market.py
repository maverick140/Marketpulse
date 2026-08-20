"""Free/public market data provider using public endpoints.

Always isolates external HTTP calls and translates errors into ProviderError
so that DataGateway can gracefully fall back to cache or demo data.
"""

from __future__ import annotations

from datetime import datetime, timezone
import httpx

from app.adapters.exceptions import ProviderError
from app.adapters.interfaces import MarketDataProvider
from app.adapters.normalized import HistoricalPricePoint, MarketIndexRecord, MarketQuote
from app.core.logging_config import get_logger

logger = get_logger("free_market")

INDEX_TICKER_MAP = {
    "NIFTY 50": "^NSEI",
    "NIFTY": "^NSEI",
    "^NSEI": "^NSEI",
    "SENSEX": "^BSESN",
    "^BSESN": "^BSESN",
    "NIFTY BANK": "^NSEBANK",
    "BANKNIFTY": "^NSEBANK",
    "^NSEBANK": "^NSEBANK",
    "NIFTY IT": "^CNXIT",
    "^CNXIT": "^CNXIT",
}


class FreeMarketProvider(MarketDataProvider):
    """Free market data provider using open public financial endpoints."""

    name = "free"
    mode = "live"

    def __init__(self, timeout_seconds: float = 6.0) -> None:
        super().__init__()
        self.timeout = timeout_seconds

    def capabilities(self) -> list[str]:
        return ["quotes", "indices", "history", "search"]

    def list_quotes(self) -> list[MarketQuote]:
        """Fetch core benchmark quotes from public Yahoo Finance v8 chart endpoint."""
        symbols = [
            ("RELIANCE", "RELIANCE.NS", "Reliance Industries Ltd", "Energy"),
            ("TCS", "TCS.NS", "Tata Consultancy Services Ltd", "Technology"),
            ("INFY", "INFY.NS", "Infosys Ltd", "Technology"),
            ("HDFCBANK", "HDFCBANK.NS", "HDFC Bank Ltd", "Financials"),
            ("ICICIBANK", "ICICIBANK.NS", "ICICI Bank Ltd", "Financials"),
            ("ITC", "ITC.NS", "ITC Ltd", "Consumer Goods"),
            ("SBIN", "SBIN.NS", "State Bank of India", "Financials"),
            ("BHARTIARTL", "BHARTIARTL.NS", "Bharti Airtel Ltd", "Telecommunications"),
            ("LT", "LT.NS", "Larsen & Toubro Ltd", "Industrials"),
            ("HINDUNILVR", "HINDUNILVR.NS", "Hindustan Unilever Ltd", "Consumer Goods"),
        ]
        quotes: list[MarketQuote] = []
        now = datetime.now(timezone.utc)

        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                for symbol, remote_ticker, name, sector in symbols:
                    try:
                        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{remote_ticker}?interval=1d&range=1d"
                        resp = client.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                        if resp.status_code == 200:
                            data = resp.json()
                            result = data.get("chart", {}).get("result", [{}])[0]
                            meta = result.get("meta", {})

                            price = meta.get("regularMarketPrice")
                            if price is None:
                                indicators = result.get("indicators", {}).get("quote", [{}])[0]
                                closes = [c for c in indicators.get("close", []) if c is not None]
                                price = closes[-1] if closes else meta.get("chartPreviousClose")

                            prev = meta.get("chartPreviousClose") or meta.get("previousClose") or price

                            if price:
                                change = round(price - prev, 2) if prev else 0.0
                                change_pct = round((change / prev) * 100, 2) if prev else 0.0
                                quotes.append(
                                    MarketQuote(
                                        symbol=symbol,
                                        name=name,
                                        price=round(float(price), 2),
                                        change=change,
                                        change_percent=change_pct,
                                        volume=meta.get("regularMarketVolume", 0) or 0,
                                        timestamp=now,
                                        provider=self.name,
                                        data_status="live",
                                        source="Yahoo Finance Public API",
                                        source_url=f"https://finance.yahoo.com/quote/{remote_ticker}",
                                        sector=sector,
                                        retrieved_at=now,
                                    )
                                )
                    except Exception as e:
                        logger.debug("Failed quote lookup for %s: %s", symbol, e)

            if not quotes:
                raise ProviderError("Free market provider returned 0 quotes")

            self._tracker.mark_available(self.capabilities())
            return quotes
        except Exception as exc:
            msg = f"FreeMarketProvider list_quotes failed: {exc.__class__.__name__}"
            self._tracker.mark_error(msg)
            raise ProviderError(msg) from exc

    def list_indices(self) -> list[MarketIndexRecord]:
        """Fetch Indian market headline indices from Yahoo Finance."""
        indices = [
            ("NIFTY 50", "^NSEI", "NIFTY 50"),
            ("SENSEX", "^BSESN", "SENSEX"),
            ("NIFTY BANK", "^NSEBANK", "NIFTY BANK"),
            ("NIFTY IT", "^CNXIT", "NIFTY IT"),
        ]
        records: list[MarketIndexRecord] = []
        now = datetime.now(timezone.utc)

        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                for symbol, remote_ticker, name in indices:
                    try:
                        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{remote_ticker}?interval=1d&range=1d"
                        resp = client.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                        if resp.status_code == 200:
                            data = resp.json()
                            result = data.get("chart", {}).get("result", [{}])[0]
                            meta = result.get("meta", {})

                            price = meta.get("regularMarketPrice")
                            if price is None:
                                indicators = result.get("indicators", {}).get("quote", [{}])[0]
                                closes = [c for c in indicators.get("close", []) if c is not None]
                                price = closes[-1] if closes else meta.get("chartPreviousClose")

                            prev = meta.get("chartPreviousClose") or meta.get("previousClose") or price

                            if price:
                                change = round(price - prev, 2) if prev else 0.0
                                change_pct = round((change / prev) * 100, 2) if prev else 0.0
                                records.append(
                                    MarketIndexRecord(
                                        symbol=symbol,
                                        name=name,
                                        value=round(float(price), 2),
                                        change=change,
                                        change_percent=change_pct,
                                        timestamp=now,
                                        provider=self.name,
                                        data_status="live",
                                        source="Yahoo Finance Public API",
                                        retrieved_at=now,
                                    )
                                )
                    except Exception as e:
                        logger.debug("Failed index lookup for %s: %s", symbol, e)

            if not records:
                raise ProviderError("Free market provider returned 0 indices")

            self._tracker.mark_available(self.capabilities())
            return records
        except Exception as exc:
            msg = f"FreeMarketProvider list_indices failed: {exc.__class__.__name__}"
            self._tracker.mark_error(msg)
            raise ProviderError(msg) from exc

    def get_quote(self, symbol: str) -> MarketQuote | None:
        """Dynamically fetch quote for any valid equity or index symbol."""
        sym_clean = symbol.strip().upper()
        now = datetime.now(timezone.utc)

        # Dynamic ticker candidates
        if sym_clean in INDEX_TICKER_MAP:
            candidates = [INDEX_TICKER_MAP[sym_clean]]
        elif "." in sym_clean or "^" in sym_clean:
            candidates = [sym_clean]
        else:
            candidates = [f"{sym_clean}.NS", f"{sym_clean}.BO", sym_clean]

        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                for remote in candidates:
                    try:
                        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{remote}?interval=1d&range=1d"
                        resp = client.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                        if resp.status_code == 200:
                            data = resp.json()
                            result = data.get("chart", {}).get("result", [{}])[0]
                            meta = result.get("meta", {})

                            price = meta.get("regularMarketPrice")
                            if price is None:
                                indicators = result.get("indicators", {}).get("quote", [{}])[0]
                                closes = [c for c in indicators.get("close", []) if c is not None]
                                price = closes[-1] if closes else meta.get("chartPreviousClose")

                            prev = meta.get("chartPreviousClose") or meta.get("previousClose") or price
                            if price:
                                change = round(price - prev, 2) if prev else 0.0
                                change_pct = round((change / prev) * 100, 2) if prev else 0.0
                                company_name = meta.get("shortName") or meta.get("longName") or sym_clean
                                exch = meta.get("exchangeName") or ("NSE" if ".NS" in remote else ("BSE" if ".BO" in remote else "Equities"))
                                return MarketQuote(
                                    symbol=sym_clean,
                                    name=company_name,
                                    price=round(float(price), 2),
                                    change=change,
                                    change_percent=change_pct,
                                    volume=meta.get("regularMarketVolume", 0) or 0,
                                    timestamp=now,
                                    provider=self.name,
                                    data_status="live",
                                    source="Yahoo Finance Public API",
                                    source_url=f"https://finance.yahoo.com/quote/{remote}",
                                    sector=exch,
                                    retrieved_at=now,
                                )
                    except Exception:
                        continue
        except Exception as exc:
            logger.debug("Dynamic quote lookup failed for %s: %s", symbol, exc)

        return None

    def search(self, query: str) -> list[MarketQuote]:
        """Dynamically search stocks/indices by company name or ticker symbol."""
        q = (query or "").strip()
        if not q:
            return self.list_quotes()

        now = datetime.now(timezone.utc)
        results: list[MarketQuote] = []
        seen_syms: set[str] = set()

        # Query Yahoo Finance Search API for real-time ticker lookup
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                url = f"https://query1.finance.yahoo.com/v1/finance/search?q={q}&quotesCount=12&newsCount=0"
                resp = client.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                if resp.status_code == 200:
                    quotes_data = resp.json().get("quotes", [])
                    for item in quotes_data:
                        raw_sym = item.get("symbol", "")
                        q_type = item.get("quoteType", "").upper()
                        if not raw_sym or q_type not in {"EQUITY", "ETF", "INDEX", "MUTUALFUND"}:
                            continue

                        # Clean display symbol
                        display_sym = raw_sym.replace(".NS", "").replace(".BO", "") if raw_sym.endswith((".NS", ".BO")) else raw_sym
                        if display_sym.upper() in seen_syms or raw_sym.upper() in seen_syms:
                            continue

                        name = item.get("shortname") or item.get("longname") or display_sym
                        exch = item.get("exchange", "")
                        sector = "NSE" if exch in {"NSI", "NSE"} else ("BSE" if exch in {"BSE", "BOM"} else (item.get("sector") or exch))

                        seen_syms.add(display_sym.upper())
                        seen_syms.add(raw_sym.upper())

                        # Construct lightweight search result quote
                        results.append(
                            MarketQuote(
                                symbol=raw_sym if (raw_sym.endswith(".NS") or raw_sym.endswith(".BO") or "^" in raw_sym) else display_sym,
                                name=name,
                                price=0.0,
                                change=0.0,
                                change_percent=0.0,
                                volume=0,
                                timestamp=now,
                                provider=self.name,
                                data_status="live",
                                source="Yahoo Finance Search",
                                sector=sector,
                                retrieved_at=now,
                            )
                        )
        except Exception as exc:
            logger.warning("Dynamic stock search API lookup failed for %s: %s", q, exc)

        return results

    def get_history(self, symbol: str, timeframe: str = "1M") -> list[HistoricalPricePoint]:
        tf_map = {
            "1D": ("1h", "1d"),
            "5D": ("1h", "5d"),
            "1M": ("1d", "1mo"),
            "3M": ("1d", "3mo"),
            "6M": ("1d", "6mo"),
            "1Y": ("1wk", "1y"),
        }
        interval, range_str = tf_map.get(timeframe.upper(), ("1d", "1mo"))
        sym_upper = symbol.strip().upper()

        if sym_upper in INDEX_TICKER_MAP:
            candidates = [INDEX_TICKER_MAP[sym_upper]]
        elif "." in sym_upper or "^" in sym_upper:
            candidates = [sym_upper]
        else:
            candidates = [f"{sym_upper}.NS", f"{sym_upper}.BO", sym_upper]

        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                for remote in candidates:
                    try:
                        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{remote}?interval={interval}&range={range_str}"
                        resp = client.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                        if resp.status_code != 200:
                            continue

                        data = resp.json()
                        result = data.get("chart", {}).get("result", [{}])[0]
                        timestamps = result.get("timestamp", [])
                        indicators = result.get("indicators", {}).get("quote", [{}])[0]
                        opens = indicators.get("open", [])
                        highs = indicators.get("high", [])
                        lows = indicators.get("low", [])
                        closes = indicators.get("close", [])
                        volumes = indicators.get("volume", [])

                        points: list[HistoricalPricePoint] = []
                        for i, ts in enumerate(timestamps):
                            c = closes[i] if i < len(closes) else None
                            if c is not None:
                                o = opens[i] if i < len(opens) and opens[i] is not None else c
                                h = highs[i] if i < len(highs) and highs[i] is not None else max(o, c)
                                l = lows[i] if i < len(lows) and lows[i] is not None else min(o, c)
                                v = volumes[i] if i < len(volumes) and volumes[i] is not None else 0
                                points.append(
                                    HistoricalPricePoint(
                                        timestamp=datetime.fromtimestamp(ts, tz=timezone.utc),
                                        open=round(float(o), 2),
                                        high=round(float(h), 2),
                                        low=round(float(l), 2),
                                        close=round(float(c), 2),
                                        volume=int(v),
                                    )
                                )
                        if points:
                            return points
                    except Exception:
                        continue

            raise ProviderError(f"No valid history points retrieved for {symbol}")
        except Exception as exc:
            msg = f"FreeMarketProvider get_history failed for {symbol}: {exc.__class__.__name__}"
            self._tracker.mark_error(msg)
            raise ProviderError(msg) from exc
