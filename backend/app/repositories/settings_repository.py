"""Concrete repository for settings persistence."""

from typing import Any

from ..database.supabase import SupabaseClient
from ..models.persistence import SettingsRecord
from .base import BaseRepository


class SettingsRepository(BaseRepository):
    def __init__(self, client: SupabaseClient | None = None) -> None:
        self._client = client or SupabaseClient()

    def get(self, key: str) -> dict[str, Any] | None:
        result = self._client.execute(lambda c: c.table("app_settings").select("*").eq("key", key).limit(1).execute())
        data = result.data or []
        return data[0] if data else None

    def upsert(self, record: SettingsRecord) -> dict[str, Any]:
        payload = record.model_dump(exclude_none=True)
        return self._client.execute(lambda c: c.table("app_settings").upsert(payload, on_conflict="key").execute())

    def save(self, entity: Any) -> Any:
        if not isinstance(entity, SettingsRecord):
            raise TypeError("SettingsRepository expects a SettingsRecord")
        return self.upsert(entity)

    def list(self, *args: Any, **kwargs: Any) -> list[Any]:
        return []
