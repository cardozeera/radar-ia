"""Concrete repository for publication persistence."""

from typing import Any

from ..database.supabase import SupabaseClient
from ..models.persistence import PublicationRecord
from .base import BaseRepository


class PublicationRepository(BaseRepository):
    def __init__(self, client: SupabaseClient | None = None) -> None:
        self._client = client or SupabaseClient()

    def create(self, record: PublicationRecord) -> dict[str, Any]:
        payload = record.model_dump(exclude_none=True)
        return self._client.execute(lambda c: c.table("publications").insert(payload).execute())

    def list_records(self) -> list[dict[str, Any]]:
        result = self._client.execute(lambda c: c.table("publications").select("*").order("created_at", desc=True).execute())
        return result.data or []

    def save(self, entity: Any) -> Any:
        if not isinstance(entity, PublicationRecord):
            raise TypeError("PublicationRepository expects a PublicationRecord")
        return self.create(entity)

    def list(self, *args: Any, **kwargs: Any) -> list[Any]:
        return self.list_records()
