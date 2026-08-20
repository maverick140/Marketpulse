"""Deterministic synthetic educational catalogs. Not live market or news data."""

from datetime import date, datetime, timedelta, timezone
import hashlib
import math

DEMO_AS_OF = datetime(2024, 6, 14, 10, 0, tzinfo=timezone.utc)
DEMO_SOURCE = "Demo Research Feed"
DEMO_MARKET_SOURCE = "Demo Market Catalog"
DEMO_MACRO_SOURCE = "Demo Macro Catalog"
DEMO_GEO_SOURCE = "Demo Geopolitical Catalog"
DEMO_ANNOUNCEMENT_SOURCE = "Demo Announcement Catalog"

DEMO_INDICES: list[dict] = [
    {
        "symbol": "NIFTY 50",
        "name": "NIFTY 50",
        "value": 23210.45,
        "change": 84.20,
        "change_percent": 0.36,
    },
    {
        "symbol": "SENSEX",
        "name": "SENSEX",
        "value": 76440.10,
        "change": 210.55,
        "change_percent": 0.28,
    },
    {
        "symbol": "NIFTY BANK",
        "name": "NIFTY BANK",
        "value": 49880.75,
        "change": -62.40,
        "change_percent": -0.12,
    },
    {
        "symbol": "NIFTY IT",
        "name": "NIFTY IT",
        "value": 35120.30,
        "change": 145.80,
        "change_percent": 0.42,
    },
]

DEMO_QUOTES: list[dict] = [
    {
        "symbol": "RELIANCE",
        "name": "Reliance Industries Ltd (demo)",
        "price": 2912.50,
        "change": 18.40,
        "change_percent": 0.64,
        "volume": 4_250_000,
        "sector": "Energy",
    },
    {
        "symbol": "TCS",
        "name": "Tata Consultancy Services Ltd (demo)",
        "price": 3854.00,
        "change": 22.15,
        "change_percent": 0.58,
        "volume": 1_820_000,
        "sector": "Technology",
    },
    {
        "symbol": "INFY",
        "name": "Infosys Ltd (demo)",
        "price": 1510.25,
        "change": 9.80,
        "change_percent": 0.65,
        "volume": 3_410_000,
        "sector": "Technology",
    },
    {
        "symbol": "HDFCBANK",
        "name": "HDFC Bank Ltd (demo)",
        "price": 1624.70,
        "change": -6.30,
        "change_percent": -0.39,
        "volume": 5_120_000,
        "sector": "Financials",
    },
    {
        "symbol": "ICICIBANK",
        "name": "ICICI Bank Ltd (demo)",
        "price": 1128.90,
        "change": 4.55,
        "change_percent": 0.40,
        "volume": 4_870_000,
        "sector": "Financials",
    },
    {
        "symbol": "ITC",
        "name": "ITC Ltd (demo)",
        "price": 432.15,
        "change": 1.20,
        "change_percent": 0.28,
        "volume": 8_640_000,
        "sector": "Consumer Goods",
    },
    {
        "symbol": "SBIN",
        "name": "State Bank of India (demo)",
        "price": 828.40,
        "change": -3.75,
        "change_percent": -0.45,
        "volume": 9_210_000,
        "sector": "Financials",
    },
    {
        "symbol": "BHARTIARTL",
        "name": "Bharti Airtel Ltd (demo)",
        "price": 1375.60,
        "change": 11.05,
        "change_percent": 0.81,
        "volume": 2_330_000,
        "sector": "Telecommunications",
    },
    {
        "symbol": "LT",
        "name": "Larsen & Toubro Ltd (demo)",
        "price": 3540.00,
        "change": 16.80,
        "change_percent": 0.48,
        "volume": 1_150_000,
        "sector": "Industrials",
    },
    {
        "symbol": "HINDUNILVR",
        "name": "Hindustan Unilever Ltd (demo)",
        "price": 2468.35,
        "change": -8.90,
        "change_percent": -0.36,
        "volume": 980_000,
        "sector": "Consumer Goods",
    },
]

DEMO_NEWS: list[dict] = [
    {
        "id": "news-demo-01",
        "headline": "Demo: Technology sector attention rises in educational sample",
        "summary": "Synthetic research note describing hypothetical software-services commentary for classroom analysis.",
        "category": "TECHNOLOGY",
        "related_entities": ["INFY", "TCS", "NIFTY IT"],
        "related_sectors": ["Technology"],
        "countries": ["India", "United States"],
        "author": "Research Staff",
        "language": "en",
    },
    {
        "id": "news-demo-02",
        "headline": "Demo: Energy theme appears in sample market briefing",
        "summary": "Synthetic briefing that links an educational energy-price scenario to listed energy-related names.",
        "category": "COMMODITIES",
        "related_entities": ["RELIANCE", "Oil"],
        "related_sectors": ["Energy"],
        "countries": ["India", "Saudi Arabia"],
        "author": "Commodity Desk",
        "language": "en",
    },
    {
        "id": "news-demo-03",
        "headline": "Demo: Banking commentary used for sentiment pipeline tests",
        "summary": "Placeholder corporate-finance narrative for NLP experiments. Not a real news item.",
        "category": "COMPANY",
        "related_entities": ["HDFCBANK", "ICICIBANK", "SBIN"],
        "related_sectors": ["Financials"],
        "countries": ["India"],
        "author": "Financial Desk",
        "language": "en",
    },
    {
        "id": "news-demo-04",
        "headline": "Demo: International trade scenario for geopolitics classroom",
        "summary": "Educational scenario describing hypothetical trade-policy discussion without citing live events.",
        "category": "GEOPOLITICS",
        "related_entities": ["Trade", "India"],
        "related_sectors": ["Industrials", "Technology"],
        "countries": ["India", "Japan"],
        "author": "Global Desk",
        "language": "en",
    },
    {
        "id": "news-demo-05",
        "headline": "Demo: Macro calendar placeholder for inflation discussion",
        "summary": "Synthetic economy note used to demonstrate category filters and provenance badges.",
        "category": "MACRO",
        "related_entities": ["Inflation", "GDP Growth"],
        "related_sectors": ["Economy"],
        "countries": ["India"],
        "author": "Macro Desk",
        "language": "en",
    },
    {
        "id": "news-demo-06",
        "headline": "Demo: Regulatory framework revisions discussed in policy simulation",
        "summary": "Educational commentary regarding capital markets compliance and governance rules.",
        "category": "REGULATORY",
        "related_entities": ["SEBI", "NSE", "BSE"],
        "related_sectors": ["Financials"],
        "countries": ["India"],
        "author": "Policy Desk",
        "language": "en",
    },
]

DEMO_MACRO: list[dict] = [
    {
        "indicator": "Inflation",
        "value": 4.8,
        "unit": "percent",
        "period": "2024-05",
        "previous_value": 4.9,
        "change": -0.1,
    },
    {
        "indicator": "Interest Rate",
        "value": 6.5,
        "unit": "percent",
        "period": "2024-06",
        "previous_value": 6.5,
        "change": 0.0,
    },
    {
        "indicator": "GDP Growth",
        "value": 6.7,
        "unit": "percent",
        "period": "2024-Q1",
        "previous_value": 6.5,
        "change": 0.2,
    },
    {
        "indicator": "Unemployment",
        "value": 7.8,
        "unit": "percent",
        "period": "2024-05",
        "previous_value": 8.0,
        "change": -0.2,
    },
    {
        "indicator": "Oil",
        "value": 82.4,
        "unit": "USD/barrel",
        "period": "2024-06-14",
        "previous_value": 81.1,
        "change": 1.3,
    },
    {
        "indicator": "Gold",
        "value": 2320.0,
        "unit": "USD/oz",
        "period": "2024-06-14",
        "previous_value": 2312.5,
        "change": 7.5,
    },
    {
        "indicator": "Currency",
        "value": 83.45,
        "unit": "INR/USD",
        "period": "2024-06-14",
        "previous_value": 83.52,
        "change": -0.07,
    },
]

DEMO_MACRO_HISTORY: dict[str, list[dict]] = {
    "inflation": [
        {"period": "2023-12", "value": 5.7, "date": date(2023, 12, 31)},
        {"period": "2024-01", "value": 5.1, "date": date(2024, 1, 31)},
        {"period": "2024-02", "value": 5.1, "date": date(2024, 2, 29)},
        {"period": "2024-03", "value": 4.9, "date": date(2024, 3, 31)},
        {"period": "2024-04", "value": 4.8, "date": date(2024, 4, 30)},
        {"period": "2024-05", "value": 4.8, "date": date(2024, 5, 31)},
    ],
    "interest rate": [
        {"period": "2023-10", "value": 6.5, "date": date(2023, 10, 31)},
        {"period": "2023-12", "value": 6.5, "date": date(2023, 12, 31)},
        {"period": "2024-02", "value": 6.5, "date": date(2024, 2, 29)},
        {"period": "2024-04", "value": 6.5, "date": date(2024, 4, 30)},
        {"period": "2024-06", "value": 6.5, "date": date(2024, 6, 14)},
    ],
    "gdp growth": [
        {"period": "2023-Q2", "value": 7.8, "date": date(2023, 6, 30)},
        {"period": "2023-Q3", "value": 7.6, "date": date(2023, 9, 30)},
        {"period": "2023-Q4", "value": 8.4, "date": date(2023, 12, 31)},
        {"period": "2024-Q1", "value": 6.7, "date": date(2024, 3, 31)},
    ],
    "unemployment": [
        {"period": "2024-01", "value": 6.8, "date": date(2024, 1, 31)},
        {"period": "2024-02", "value": 8.0, "date": date(2024, 2, 29)},
        {"period": "2024-03", "value": 7.6, "date": date(2024, 3, 31)},
        {"period": "2024-04", "value": 8.1, "date": date(2024, 4, 30)},
        {"period": "2024-05", "value": 7.8, "date": date(2024, 5, 31)},
    ],
    "oil": [
        {"period": "2024-01", "value": 78.3, "date": date(2024, 1, 31)},
        {"period": "2024-02", "value": 81.6, "date": date(2024, 2, 29)},
        {"period": "2024-03", "value": 85.4, "date": date(2024, 3, 31)},
        {"period": "2024-04", "value": 89.0, "date": date(2024, 4, 30)},
        {"period": "2024-05", "value": 83.5, "date": date(2024, 5, 31)},
        {"period": "2024-06-14", "value": 82.4, "date": date(2024, 6, 14)},
    ],
    "gold": [
        {"period": "2024-01", "value": 2040.0, "date": date(2024, 1, 31)},
        {"period": "2024-02", "value": 2055.0, "date": date(2024, 2, 29)},
        {"period": "2024-03", "value": 2160.0, "date": date(2024, 3, 31)},
        {"period": "2024-04", "value": 2330.0, "date": date(2024, 4, 30)},
        {"period": "2024-05", "value": 2345.0, "date": date(2024, 5, 31)},
        {"period": "2024-06-14", "value": 2320.0, "date": date(2024, 6, 14)},
    ],
    "currency": [
        {"period": "2024-01", "value": 83.15, "date": date(2024, 1, 31)},
        {"period": "2024-02", "value": 82.95, "date": date(2024, 2, 29)},
        {"period": "2024-03", "value": 83.35, "date": date(2024, 3, 31)},
        {"period": "2024-04", "value": 83.45, "date": date(2024, 4, 30)},
        {"period": "2024-05", "value": 83.30, "date": date(2024, 5, 31)},
        {"period": "2024-06-14", "value": 83.45, "date": date(2024, 6, 14)},
    ],
}

DEMO_EVENTS: list[dict] = [
    {
        "id": "geo-demo-01",
        "title": "Demo: Hypothetical trade-policy discussion in South Asia",
        "description": "Exploratory scenario detailing bilateral trade discussions and regional supply chain adjustments.",
        "region": "South Asia",
        "country": "India",
        "category": "Trade",
        "severity": 45,
        "market_relevance": 60,
        "related_sectors": ["Energy", "Technology"],
        "affected_assets": ["NIFTY 50", "Currency"],
    },
    {
        "id": "geo-demo-02",
        "title": "Demo: Educational energy-supply scenario for Middle East classroom",
        "description": "Simulation analyzing shipping lane monitoring and energy commodity price sensitivity.",
        "region": "Middle East",
        "country": "Regional sample",
        "category": "Energy",
        "severity": 70,
        "market_relevance": 75,
        "related_sectors": ["Energy"],
        "affected_assets": ["Oil", "RELIANCE"],
    },
    {
        "id": "geo-demo-03",
        "title": "Demo: Synthetic regulation workshop in Europe",
        "description": "Classroom scenario on cross-border data protection directives affecting technology exporters.",
        "region": "Europe",
        "country": "Regional sample",
        "category": "Regulation",
        "severity": 35,
        "market_relevance": 40,
        "related_sectors": ["Finance", "Technology"],
        "affected_assets": ["INFY", "TCS"],
    },
    {
        "id": "geo-demo-04",
        "title": "Demo: Diplomacy tabletop exercise in East Asia",
        "description": "Regional strategic cooperation discussions centered on semiconductor supply chains.",
        "region": "East Asia",
        "country": "Regional sample",
        "category": "Diplomacy",
        "severity": 50,
        "market_relevance": 55,
        "related_sectors": ["Technology", "Supply Chain"],
        "affected_assets": ["NIFTY IT"],
    },
    {
        "id": "geo-demo-05",
        "title": "Demo: Supply-chain tabletop for North America",
        "description": "Simulation assessing port automation and freight rate trends across major trade corridors.",
        "region": "North America",
        "country": "Regional sample",
        "category": "Supply Chain",
        "severity": 40,
        "market_relevance": 50,
        "related_sectors": ["Technology", "Energy"],
        "affected_assets": ["LT"],
    },
]

DEMO_ANNOUNCEMENTS: list[dict] = [
    {
        "id": "ann-demo-01",
        "title": "Demo: Sample corporate results briefing (synthetic)",
        "category": "COMPANY",
        "announcement_type": "ANNOUNCEMENT",
        "date": date(2024, 6, 10),
        "importance": "medium",
        "related_sectors": ["Technology"],
        "related_entities": ["TCS", "INFY"],
    },
    {
        "id": "ann-demo-02",
        "title": "Demo: Educational macro-calendar placeholder",
        "category": "ECONOMY",
        "announcement_type": "OFFICIAL_RELEASE",
        "date": date(2024, 6, 12),
        "importance": "high",
        "related_sectors": ["Financials"],
        "related_entities": ["Inflation", "GDP"],
    },
    {
        "id": "ann-demo-03",
        "title": "Demo: Synthetic regulatory-process note",
        "category": "REGULATORY",
        "announcement_type": "OFFICIAL_RELEASE",
        "date": date(2024, 6, 8),
        "importance": "medium",
        "related_sectors": ["Financials"],
        "related_entities": ["SEBI"],
    },
    {
        "id": "ann-demo-04",
        "title": "Demo: Classroom central-bank communication sample",
        "category": "POLICY",
        "announcement_type": "OFFICIAL_RELEASE",
        "date": date(2024, 6, 7),
        "importance": "high",
        "related_sectors": ["Financials"],
        "related_entities": ["RBI", "Interest Rate"],
    },
    {
        "id": "ann-demo-05",
        "title": "Demo: Government process overview (non-official)",
        "category": "POLICY",
        "announcement_type": "ANNOUNCEMENT",
        "date": date(2024, 6, 5),
        "importance": "low",
        "related_sectors": ["Industrials"],
        "related_entities": ["LT"],
    },
]


def generate_demo_history(base_price: float, timeframe: str = "1M") -> list[dict]:
    """Deterministically generate OHLCV candles based on base_price and timeframe."""
    normalized_tf = (timeframe or "1M").upper()
    points_config = {
        "1D": (24, timedelta(hours=1)),
        "5D": (30, timedelta(hours=4)),
        "1M": (30, timedelta(days=1)),
        "3M": (45, timedelta(days=2)),
        "6M": (60, timedelta(days=3)),
        "1Y": (52, timedelta(days=7)),
    }
    count, step = points_config.get(normalized_tf, (30, timedelta(days=1)))
    end_time = DEMO_AS_OF
    start_time = end_time - (step * (count - 1))

    candles: list[dict] = []
    current_price = base_price * 0.92

    for i in range(count):
        t = start_time + (step * i)
        wave = math.sin(i * 0.45) * 0.015 + math.cos(i * 0.25) * 0.01
        drift = 0.002 * (i / count)
        step_change = current_price * (wave + drift)
        open_p = round(current_price, 2)
        close_p = round(max(current_price + step_change, 1.0), 2)
        spread = abs(close_p - open_p) + (base_price * 0.005)
        high_p = round(max(open_p, close_p) + (spread * 0.6), 2)
        low_p = round(min(open_p, close_p) - (spread * 0.5), 2)
        vol = int(abs(math.sin(i * 0.8)) * 500_000 + 100_000)

        candles.append({
            "timestamp": t,
            "open": open_p,
            "high": high_p,
            "low": low_p,
            "close": close_p,
            "volume": vol,
        })
        current_price = close_p

    if candles:
        candles[-1]["close"] = round(base_price, 2)
        candles[-1]["high"] = round(max(candles[-1]["high"], base_price), 2)
        candles[-1]["low"] = round(min(candles[-1]["low"], base_price), 2)

    return candles
