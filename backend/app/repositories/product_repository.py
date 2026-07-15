"""Concrete repository for product persistence."""

from typing import Any

from ..database.supabase import SupabaseClient
from ..models.persistence import ProductRecord
from .base import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self, client: SupabaseClient | None = None) -> None:
        self._client = client or SupabaseClient()

    def upsert_product(self, product: ProductRecord) -> dict[str, Any]:
        payload = product.model_dump(exclude_none=True)
        return self._client.execute(lambda c: c.table("products").upsert(payload, on_conflict="provider,external_id").execute())

    def get_product_by_external_id(self, provider: str, external_id: str) -> dict[str, Any] | None:
        result = self._client.execute(lambda c: c.table("products").select("*").eq("provider", provider).eq("external_id", external_id).limit(1).execute())
        return (result.data or [None])[0]

    def list_products(self, limit: int = 100) -> list[dict[str, Any]]:
        result = self._client.execute(lambda c: c.table("products").select("*").order("created_at", desc=True).limit(limit).execute())
        return result.data or []

    def count_products(self) -> int:
        result = self._client.execute(lambda c: c.table("products").select("id", count="exact").execute())
        return int(getattr(result, "count", 0) or 0)

    def save(self, entity: Any) -> Any:
        if not isinstance(entity, ProductRecord):
            raise TypeError("ProductRepository expects a ProductRecord")
        return self.upsert_product(entity)

    def list(self, *args: Any, **kwargs: Any) -> list[Any]:
        return self.list_products(limit=kwargs.get("limit", 100))
