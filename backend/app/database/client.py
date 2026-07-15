"""Database client wrapper for Supabase access."""

from typing import Any

from supabase import create_client

from ..core.settings import settings


class DatabaseClient:
    """Centralized Supabase client with explicit validation and error handling."""

    def __init__(self, url: str | None = None, key: str | None = None) -> None:
        self._url = self._normalize_url(url or settings.supabase_url)
        self._key = (key or settings.supabase_secret_key).strip()
        self._client: Any | None = None

    def _normalize_url(self, url: str) -> str:
        value = (url or "").strip()
        if not value:
            return ""
        value = value.rstrip("/")
        if value.endswith("/rest/v1"):
            value = value[: -len("/rest/v1")]
        return value.rstrip("/")

    def validate_configuration(self) -> None:
        if not self._url or not self._key:
            raise RuntimeError("Supabase configuration is incomplete. Set SUPABASE_URL and SUPABASE_SECRET_KEY.")

    def get_client(self) -> Any:
        self.validate_configuration()
        if self._client is None:
            self._client = create_client(self._url, self._key)
        return self._client

    def ping(self) -> bool:
        try:
            self.get_client()
            return True
        except Exception:
            return False

    def execute(self, operation: Any) -> Any:
        try:
            return operation(self.get_client())
        except Exception as exc:
            raise RuntimeError(f"Supabase operation failed: {exc}") from exc
