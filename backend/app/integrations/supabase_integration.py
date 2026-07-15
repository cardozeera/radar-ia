"""Supabase integration adapter."""

from typing import Any

from .base import BaseIntegration


class SupabaseIntegration(BaseIntegration):
    """Adapter that encapsulates Supabase access."""

    def __init__(self, settings: Any) -> None:
        self._settings = settings

    def connect(self) -> Any:
        return {"status": "not_implemented", "settings": self._settings.model_dump()}
