from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import structlog
import logging

from src.core.config import settings
from src.core.exceptions import register_exception_handlers
from src.routers.jobs import router as jobs_router
from src.routers.screener import router as screener_router
from src.routers.export import router as export_router
from src.db.session import engine
from src.db.base import Base
from src.models.job import JobDescription, MatchResult, SkillScore
from src.models.candidate import Candidate, ResumeFile, ExtractionData

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup lifecycle events: Automatically ensure database tables are created
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("database_tables_ensured_created")
    except Exception as e:
        logger.error("database_startup_creation_failed", error=str(e))

    logger.info("application_startup", app_name=settings.app_name, environment=settings.environment)
    yield
    # Shutdown lifecycle events
    logger.info("application_shutdown", app_name=settings.app_name)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="Enterprise-grade AI & Hybrid Resume Screening & Candidate Matching Platform",
        lifespan=lifespan,
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register Exception Handlers
    register_exception_handlers(app)

    # Include API Routers
    app.include_router(jobs_router)
    app.include_router(screener_router)
    app.include_router(export_router)

    @app.get("/", include_in_schema=False)
    async def root_redirect():
        """
        Redirects root URL directly to comprehensive Swagger UI (/docs).
        """
        return RedirectResponse(url="/docs", status_code=303)

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "healthy", "app": settings.app_name, "environment": settings.environment}

    return app

app = create_app()
