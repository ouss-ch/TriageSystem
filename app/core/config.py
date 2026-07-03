"""Centralized app settings, loaded from environment / .env."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "TriageSystem"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    EMAIL_HOST: str = ""
    EMAIL_PORT: int = 993
    EMAIL_USER: str = ""
    EMAIL_PASSWORD: str = ""
    EMAIL_MAILBOX: str = "INBOX"

    LLM_PROVIDER: str = "anthropic"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "claude-sonnet-5"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
