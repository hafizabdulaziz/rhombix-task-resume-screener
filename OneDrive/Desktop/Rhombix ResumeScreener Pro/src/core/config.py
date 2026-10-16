import logging
import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
import structlog

class Settings(BaseSettings):
    PROJECT_NAME: str = "Rhombix ResumeScreener Pro"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite+aiosqlite:///./resumescreener.db"
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "recruiter@rhombix.com"
    SMTP_PASSWORD: str = "securepassword"
    EMAILS_FROM_EMAIL: str = "recruiter@rhombix.com"
    UPLOAD_DIR: str = "storage/uploads"
    EXPORT_DIR: str = "storage/exports"
    MAX_UPLOAD_SIZE_MB: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

def configure_logging():
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
    )
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer() if not settings.DEBUG else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

configure_logging()
