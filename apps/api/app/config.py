# OpenSchoolOS API — runtime settings (Sprint 001).
# Infrastructure layer. Reads DATABASE_URL from environment; no secrets,
# no auth in Sprint 1 (tech-stack.md).
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://openschoolos:openschoolos@localhost:5432/openschoolos"


settings = Settings()
