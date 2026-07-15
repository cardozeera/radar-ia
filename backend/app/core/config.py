"""Central configuration placeholders for environment-based settings."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = "Radar IA"
    environment: str = os.getenv("ENVIRONMENT", "development")
    supabase_url: str | None = os.getenv("SUPABASE_URL")
    supabase_key: str | None = os.getenv("SUPABASE_KEY")


settings = Settings()
