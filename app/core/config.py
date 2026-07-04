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

    EMAIL_MAILBOX: str = "INBOX"

    # Fernet key used to encrypt/decrypt mailbox passwords stored via /sweepers.
    ENCRYPTION_KEY: str

    # JWT signing for /auth login sessions.
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    LLM_BASE_URL: str = "http://llm:8000/v1"
    LLM_API_KEY: str = "not-needed"
    LLM_MODEL: str = "Qwen/Qwen2.5-0.5B-Instruct"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
