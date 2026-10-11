# MarketPulse AI — Agent Instructions

## Source of Truth

- `PROJECT_SPEC.md` is the authoritative product and architecture specification.
- `docs/PROJECT_STATE.md` is the authoritative implementation status.
- The actual repository and passing tests are the final verification source.

Always read PROJECT_SPEC.md and docs/PROJECT_STATE.md before substantial implementation work.

## Development Rules

- This is an existing project, NOT a greenfield project.
- Never rebuild completed phases.
- Never delete working functionality to simplify implementation.
- Implement only the current requested phase.
- Preserve backward compatibility with completed phases.
- Run the complete test suite after substantial changes.
- Never mark a phase complete without actually running and validating it.

## Architecture

Maintain the layered architecture:

API Routes
→ Pydantic Schemas
→ Services
→ Provider Gateway / Registry
→ Providers
→ Validation / Normalization
→ SQLite Persistence / Cache

Do not put provider-specific HTTP/API logic directly inside FastAPI routes.

Keep external providers replaceable through provider interfaces.

## Data Sources

- The application must remain functional without paid APIs.
- Prefer genuinely free/public data sources.
- Never hardcode API keys or secrets.
- Store optional credentials only through environment variables.
- Never commit `.env`, credentials, or secrets.
- Demo mode must work without external credentials.

Synthetic data must always be clearly marked:

`data_status = "demo"`

Never represent synthetic/demo data as live data.

Cached data must be clearly distinguishable from live data.

## Error Handling

External provider failures must not crash the application.

Use the existing fallback architecture:

Primary Provider
→ Validation
→ Cache
→ Demo Fallback

Use structured application errors.

Do not expose stack traces or secrets through API responses.

## Testing

- Never delete tests simply to make the suite pass.
- Preserve all completed-phase regression tests.
- Run the complete test suite after substantial changes.
- Test both successful and failure/fallback paths.
- Only report PASS when actually verified.

## Portfolio Quality

This is a student portfolio/GitHub project.

Prefer:

- readable code
- explainable architecture
- modular services
- meaningful names
- tests
- documentation
- transparent data provenance
- reproducible demo mode
- sensible dependency choices

Avoid unnecessary enterprise complexity.

## Scope Control

Do not implement future phases prematurely.

In particular, do not implement React/frontend, news intelligence, NLP/sentiment, geopolitical intelligence, advanced analytics/risk, or AI research features unless explicitly required by the current phase.
