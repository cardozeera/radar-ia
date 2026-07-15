"""Concrete repository for price history persistence."""

from typing import Any

from ..database.supabase import SupabaseClient
from ..models.persistence import PriceHistoryRecord
from .base import BaseRepository


class PriceHistoryRepository(BaseRepository):
    def __init__(self, client: SupabaseClient | None = None) -> None:
        self._client = client or SupabaseClient()

    def add_price(self, record: PriceHistoryRecord) -> dict[str, Any]:
        payload = record.model_dump(exclude_none=True)
        return self._client.execute(lambda c: c.table("price_history").insert(payload).execute())

    def list_recent(self, limit: int = 50) -> list[dict[str, Any]]:
        result = self._client.execute(lambda c: c.table("price_history").select("*").order("collected_at", desc=True).limit(limit).execute())
        return result.data or []

    def list_by_product(self, product_id: str) -> list[dict[str, Any]]:
        result = self._client.execute(lambda c: c.table("price_history").select("*").eq("product_id", product_id).order("collected_at", desc=True).execute())
        return result.data or []

    def save(self, entity: Any) -> Any:
        if not isinstance(entity, PriceHistoryRecord):
            raise TypeError("PriceHistoryRepository expects a PriceHistoryRecord")
        return self.add_price(entity)

    def list(self, *args: Any, **kwargs: Any) -> list[Any]:
        return self.list_recent(limit=kwargs.get("limit", 50))
