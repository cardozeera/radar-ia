"""Concrete repository for watchlist persistence."""

from typing import Any

from ..database.supabase import SupabaseClient
from ..models.persistence import WatchlistRecord
from .base import BaseRepository


class WatchlistRepository(BaseRepository):
    def __init__(self, client: SupabaseClient | None = None) -> None:
        self._client = client or SupabaseClient()

    def add(self, record: WatchlistRecord) -> dict[str, Any]:
        payload = record.model_dump(exclude_none=True)
        return self._client.execute(lambda c: c.table("watchlist").upsert(payload, on_conflict="provider,external_id").execute())

    def list_records(self) -> list[dict[str, Any]]:
        result = self._client.execute(lambda c: c.table("watchlist").select("*").order("created_at", desc=True).execute())
        return result.data or []

    def remove(self, external_id: str, provider: str = "mercadolivre") -> None:
        self._client.execute(lambda c: c.table("watchlist").delete().eq("provider", provider).eq("external_id", external_id).execute())

    def update_last_price(self, external_id: str, price: float, provider: str = "mercadolivre") -> None:
        self._client.execute(lambda c: c.table("watchlist").update({"last_price": price, "last_checked_at": "now()"}).eq("provider", provider).eq("external_id", external_id).execute())

    def save(self, entity: Any) -> Any:
        if not isinstance(entity, WatchlistRecord):
            raise TypeError("WatchlistRepository expects a WatchlistRecord")
        return self.add(entity)

    def list(self, *args: Any, **kwargs: Any) -> list[Any]:
        return self.list_records()
