from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Rhombix ResumeScreener Pro"
    environment: str = "development"
    debug: bool = True
    api_v1_str: str = "/api/v1"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/rhombix_resume_screener"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "supersecretkeychangemeinproduction"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
