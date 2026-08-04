# OpenSchoolOS API — runtime settings (Sprint 005).
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./openschoolos.db"
    jwt_secret: str = "change-me-in-production-use-a-strong-random-secret"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 24 hours


settings = Settings()
