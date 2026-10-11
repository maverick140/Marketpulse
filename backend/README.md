# MarketPulse AI — Backend

Student-friendly guide to the FastAPI backend for **MarketPulse AI**, an educational financial and geopolitical intelligence platform.

This backend is a research demonstration. It does **not** provide investment advice, brokerage, or trade execution.

## Purpose

Phase 1 establishes the backend **foundation** only:

- FastAPI application
- Environment configuration
- Logging and structured errors
- SQLite + SQLAlchemy setup
- Health and system status endpoints
- pytest coverage for those endpoints

Phase 2 adds domain models, replaceable data providers, demo catalogs, a provider registry, SQLite persistence/cache, and fallback when a provider fails.

Later phases will add market/news APIs, NLP, geopolitics analytics, and the AI research engine.

## Architecture

The backend uses a layered layout:

```
API routes  →  Pydantic schemas  →  Services  →  Database / cache  →  Providers
```

Provider flow:

```
Primary provider → validation → SQLite cache → demo fallback
```

| Folder | Role |
|---|---|
| `app/api/routes` | Thin HTTP handlers |
| `app/schemas` | Request/response models |
| `app/services` | Business logic |
| `app/database` | Engine, session, domain models, persistence/cache |
| `app/core` | Config, logging, errors |
| `app/adapters` | Provider interfaces, demo/failing adapters, registry, gateway |
| `app/analytics` | Financial analytics (later) |
| `app/ml` | NLP / ML (later) |

Keep logic out of route files. Routes call services; services use the database or adapters.

## Setup

Work from the `backend` directory.

### Virtual environment

Windows (PowerShell):

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
```

### Installation

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

No API keys are required.

### Environment configuration

Copy the example file and edit if needed:

```powershell
copy .env.example .env
```

Important variables:

| Variable | Meaning | Default |
|---|---|---|
| `APP_NAME` | Application title | `MarketPulse AI` |
| `APP_ENV` | `development` or `production` | `development` |
| `APP_VERSION` | API version reported by `/api/system/status` | `0.1.0` |
| `DATA_MODE` | `demo` selects demo providers by default | `demo` |
| `MARKET_PROVIDER` | Market adapter name (`demo`) | `demo` |
| `NEWS_PROVIDER` | News adapter name | `demo` |
| `MACRO_PROVIDER` | Macro adapter name | `demo` |
| `GEOPOLITICAL_PROVIDER` | Geopolitics adapter name | `demo` |
| `ANNOUNCEMENT_PROVIDER` | Announcements adapter name | `demo` |
| `DATABASE_URL` | SQLAlchemy URL | `sqlite:///./marketpulse.db` |
| `CORS_ORIGINS` | Comma-separated Vite origins | `http://localhost:5173,http://127.0.0.1:5173` |
| `LOG_LEVEL` | Logging level | `INFO` |

Do not put real secrets in Git. Optional API keys will be added later and must stay empty for demo mode.

## Database

SQLAlchemy uses **SQLite** by default. The file `marketpulse.db` is created next to the backend package on startup.

Phase 2 creates domain tables including companies, securities, market prices, indices, news, sentiment results, countries, geopolitical events, announcements, macro indicators, AI insights, data sources, audit logs, watchlist items, and saved research.

SQLite is also the first cache layer. If a future live provider fails, the gateway can return cached rows, then demo data, without crashing.

## Providers

`DATA_MODE=demo` (and `*_PROVIDER=demo`) uses deterministic educational catalogs. Records are labeled `data_status=demo` and never presented as live data. Demo news uses source `Demo Research Feed` and does not invent real publication URLs.

The registry constructs market, news, macro, geopolitical, and announcement providers from configuration. Routes must not select providers themselves.

## Running FastAPI

From `backend` with the virtual environment active:

```powershell
uvicorn app.main:app --reload
```

Then open:

- API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)
- System providers: [http://127.0.0.1:8000/api/system/providers](http://127.0.0.1:8000/api/system/providers)

Example health response:

```json
{
  "status": "ok",
  "service": "MarketPulse AI"
}
```

## Testing

From `backend`:

```powershell
python -m pytest
```

Tests cover health, system status, database models, demo providers, registry selection, normalization, fallback, and `/api/system/providers`.
