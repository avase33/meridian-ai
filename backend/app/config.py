"""Application configuration via Pydantic Settings."""

from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    # Core
    app_name: str = "Meridian AI"
    environment: str = "development"
    debug: bool = False
    secret_key: str
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Database
    database_url: str
    db_pool_size: int = 10
    db_max_overflow: int = 20

    # Redis / Celery
    redis_url: str
    celery_broker_url: str = ""
    celery_result_backend: str = ""

    # LLM
    anthropic_api_key: str
    llm_model: str = "claude-opus-4-8"
    llm_max_tokens: int = 4096
    llm_temperature: float = 0.1

    # CORS
    allowed_origins: List[str] = ["http://localhost:3000"]

    # Agent Limits
    max_agents_per_org: int = 50
    max_concurrent_runs: int = 10
    agent_timeout_seconds: int = 300

    # Observability
    otel_endpoint: str = ""
    log_level: str = "INFO"

    @field_validator("celery_broker_url", mode="before")
    @classmethod
    def set_celery_broker(cls, v: str, info) -> str:
        return v or info.data.get("redis_url", "")

    @field_validator("celery_result_backend", mode="before")
    @classmethod
    def set_celery_backend(cls, v: str, info) -> str:
        return v or info.data.get("redis_url", "")

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()