from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
import structlog
import logging

from src.core.config import settings
from src.core.exceptions import register_exception_handlers
from src.routers.jobs import router as jobs_router
from src.routers.upload import router as upload_router
from src.routers.screener import router as screener_router
from src.routers.export import router as export_router
from src.routers.tasks import router as tasks_router
from src.routers.auth import router as auth_router
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
        description="Enterprise-grade AI & Hybrid Resume Screening & Candidate Matching Platform (Silver Swagger Edition)",
        docs_url=None, # Disabled default docs to serve customized silver swagger ui
        redoc_url=None,
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

    # Include API Routers in Ordered Sequence
    app.include_router(jobs_router)
    app.include_router(upload_router)
    app.include_router(screener_router)
    app.include_router(export_router)
    app.include_router(tasks_router)
    app.include_router(auth_router)

    @app.get("/docs", include_in_schema=False)
    async def custom_silver_swagger_ui():
        html_response = get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Silver Enterprise UI",
            swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        )
        custom_css = """
        <style>
        body { background-color: #f8fafc !important; font-family: 'Inter', sans-serif !important; }
        .swagger-ui .topbar { background-color: #1e293b !important; border-bottom: 2px solid #334155; }
        .swagger-ui .info h1 { color: #0f172a; font-weight: 700; }
        .swagger-ui .scheme-container { background: #e2e8f0; border-bottom: 1px solid #cbd5e1; box-shadow: none; }
        .swagger-ui .btn.execute { background-color: #2563eb; color: white; border-radius: 6px; }
        .swagger-ui .btn.execute:hover { background-color: #1d4ed8; }
        </style>
        """
        html_content = html_response.body.decode("utf-8")
        html_content = html_content.replace("</head>", custom_css + "</head>")
        return HTMLResponse(content=html_content)

    @app.get("/", include_in_schema=False)
    async def root_redirect():
        """
        Redirects root URL directly to comprehensive Silver Swagger UI (/docs).
        """
        return RedirectResponse(url="/docs", status_code=303)

    @app.get("/health", tags=["System Health & Performance Monitoring"])
    async def health_check():
        return {"status": "healthy", "app": settings.app_name, "environment": settings.environment}

    return app

app = create_app()
