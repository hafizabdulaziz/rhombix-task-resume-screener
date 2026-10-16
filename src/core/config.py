import logging
import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
import structlog

class Settings(BaseSettings):
    app_name: str = "Rhombix ResumeScreener Pro"
    project_name: str = "Rhombix ResumeScreener Pro"
    environment: str = "development"
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./resumescreener.db"
    api_v1_str: str = "/api/v1"
    smtp_host: str = "smtp.example.com"
    smtp_port: int = 587
    smtp_user: str = "recruiter@rhombix.com"
    smtp_password: str = "securepassword"
    emails_from_email: str = "recruiter@rhombix.com"
    smtp_from_email: str = "recruiter@rhombix.com"
    upload_dir: str = "storage/uploads"
    export_dir: str = "storage/exports"
    max_upload_size_mb: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

settings = Settings()

def configure_logging():
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG if settings.debug else logging.INFO,
    )
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer() if not settings.debug else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

configure_logging()
