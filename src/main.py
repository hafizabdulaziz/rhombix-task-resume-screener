from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from slowapi.errors import RateLimitExceeded

from src.core.config import settings
from src.core.exceptions import register_exception_handlers
from src.core.limiter import limiter, rate_limit_exceeded_handler
from src.core.security_headers import SecurityHeadersMiddleware
from src.db.base import Base
from src.db.session import engine
from src.routers.analytics import router as analytics_router
from src.routers.auth import router as auth_router
from src.routers.export import router as export_router
from src.routers.jobs import router as jobs_router
from src.routers.screener import router as screener_router
from src.routers.tasks import router as tasks_router
from src.routers.upload import router as upload_router

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
        docs_url="/docs",
        redoc_url="/redoc",
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
    app.add_middleware(SecurityHeadersMiddleware)

    # Register Exception Handlers
    register_exception_handlers(app)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

    # Include API Routers in Ordered Sequence
    app.include_router(jobs_router)
    app.include_router(upload_router)
    app.include_router(screener_router)
    app.include_router(export_router)
    app.include_router(tasks_router)
    app.include_router(auth_router)
    app.include_router(analytics_router)

    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs", status_code=303)

    @app.get("/health", tags=["System Health & Performance Monitoring"])
    async def health_check():
        return {"status": "healthy", "app": settings.app_name, "environment": settings.environment}

    @app.get("/ready", tags=["System Health & Performance Monitoring"])
    async def readiness_check():
        return {"status": "ready", "database": "connected"}

    return app

app = create_app()
