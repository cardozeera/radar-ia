"""Application settings centralized in one module."""

import os
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


# Caminho absoluto para backend/.env
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


def _load_env_file() -> None:
    """Carrega o arquivo .env sobrescrevendo variáveis antigas."""

    print(f"[Radar IA] Carregando .env em: {ENV_PATH}")

    if not ENV_PATH.exists():
        print("[Radar IA] Arquivo .env não encontrado.")
        return

    for raw_line in ENV_PATH.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)

        key = key.strip()
        value = value.strip().strip('"').strip("'")

        # Sempre sobrescreve a variável do ambiente
        os.environ[key] = value

    print("[Radar IA] .env carregado com sucesso.")


_load_env_file()


class Settings(BaseModel):
    app_name: str = Field(default="Radar IA")
    environment: str = Field(default="development")

    supabase_url: str = Field(default="")
    supabase_secret_key: str = Field(default="")

    provider_timeout_seconds: int = Field(default=15)
    enable_mock_providers: bool = Field(default=True)

    @field_validator("supabase_url")
    @classmethod
    def validate_supabase_url(cls, value: str) -> str:
        return value.strip()

    @field_validator("supabase_secret_key")
    @classmethod
    def validate_supabase_secret_key(cls, value: str) -> str:
        return value.strip()

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("RADAR_IA_APP_NAME", "Radar IA"),
            environment=os.getenv("RADAR_IA_ENVIRONMENT", "development"),
            supabase_url=os.getenv("SUPABASE_URL", ""),
            supabase_secret_key=os.getenv(
                "SUPABASE_SECRET_KEY",
                os.getenv("SUPABASE_KEY", "")
            ),
            provider_timeout_seconds=int(
                os.getenv("RADAR_IA_PROVIDER_TIMEOUT_SECONDS", "15")
            ),
            enable_mock_providers=os.getenv(
                "RADAR_IA_ENABLE_MOCK_PROVIDERS",
                "true"
            ).lower() == "true",
        )


settings = Settings.from_env()

print("=" * 60)
print("RADAR IA SETTINGS")
print(f"SUPABASE URL: {settings.supabase_url}")
print(f"SUPABASE KEY LENGTH: {len(settings.supabase_secret_key)}")
print("=" * 60)