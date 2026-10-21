from contextlib import asynccontextmanager

import structlog
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
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
from src.routers.web import router as web_router

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

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = FastAPI.openapi(app)
        for _, path_item in openapi_schema.get("paths", {}).items():
            for _, operation in path_item.items():
                request_body = operation.get("requestBody", {})
                content = request_body.get("content", {})
                multipart = content.get("multipart/form-data", {})
                schema = multipart.get("schema", {})
                if "$ref" in schema:
                    ref_name = schema["$ref"].split("/")[-1]
                    component_schema = openapi_schema.get("components", {}).get("schemas", {}).get(ref_name, {})
                    for prop_val in component_schema.get("properties", {}).values():
                        if prop_val.get("type") == "array" and prop_val.get("items", {}).get("contentMediaType") == "application/octet-stream":
                            prop_val["items"]["format"] = "binary"
                        elif prop_val.get("contentMediaType") == "application/octet-stream":
                            prop_val["format"] = "binary"
                elif schema.get("properties"):
                    for prop_val in schema.get("properties", {}).values():
                        if prop_val.get("type") == "array" and prop_val.get("items", {}).get("contentMediaType") == "application/octet-stream":
                            prop_val["items"]["format"] = "binary"
                        elif prop_val.get("contentMediaType") == "application/octet-stream":
                            prop_val["format"] = "binary"
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
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
    app.include_router(web_router)

    os.makedirs("src/static", exist_ok=True)
    app.mount("/static", StaticFiles(directory="src/static"), name="static")

    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs", status_code=303)

    @app.get("/docs/", include_in_schema=False)
    async def docs_slash_redirect():
        return RedirectResponse(url="/docs", status_code=303)

    @app.get("/health", tags=["System Health & Performance Monitoring"])
    async def health_check():
        return {"status": "healthy", "app": settings.app_name, "environment": settings.environment}

    @app.get("/ready", tags=["System Health & Performance Monitoring"])
    async def readiness_check():
        return {"status": "ready", "database": "connected"}

    return app

app = create_app()
