"""MarketPulse AI FastAPI application."""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.ai import router as ai_router
from app.api.routes.alerts import router as alerts_router
from app.api.routes.announcements import router as announcements_router
from app.api.routes.geopolitics import router as geopolitics_router
from app.api.routes.health import router as health_router
from app.api.routes.macro import router as macro_router
from app.api.routes.markets import router as markets_router
from app.api.routes.news import router as news_router
from app.api.routes.risk import router as risk_router
from app.api.routes.search import router as search_router
from app.api.routes.sentiment import router as sentiment_router
from app.api.routes.system import router as system_router
from app.api.routes.user import router as user_router
from app.core.config import get_settings
from app.core.error_handling import register_error_handlers
from app.core.logging_config import configure_logging, get_logger
from app.database.database import init_db

configure_logging()
logger = get_logger("main")
settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    logger.info(
        "Starting %s (env=%s, data_mode=%s, version=%s)",
        settings.app_name,
        settings.app_env,
        settings.data_mode,
        settings.app_version,
    )
    db_initialized = init_db()
    if not db_initialized:
        logger.info("Decoupled in-memory operational mode active")
    yield
    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    description=(
        "Student-built educational financial and geopolitical intelligence "
        "platform. This API is a research demonstration, not investment advice."
    ),
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)
app.include_router(health_router, prefix="/api")
app.include_router(system_router, prefix="/api/system")
app.include_router(markets_router, prefix="/api/markets")
app.include_router(macro_router, prefix="/api/macro")
app.include_router(news_router, prefix="/api/news")
app.include_router(announcements_router, prefix="/api/announcements")
app.include_router(sentiment_router, prefix="/api/sentiment")
app.include_router(geopolitics_router, prefix="/api/geopolitics")
app.include_router(ai_router, prefix="/api/ai")
app.include_router(risk_router, prefix="/api/risk")
app.include_router(alerts_router, prefix="/api/alerts")
app.include_router(search_router, prefix="/api/search")
app.include_router(user_router, prefix="/api/user")
