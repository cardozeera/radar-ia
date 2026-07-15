"""Service that orchestrates the Mercado Livre provider."""

from typing import Any

from ..providers.mercadolivre.client import MercadoLivreProvider


class MercadoLivreService:
    def __init__(self, provider: MercadoLivreProvider | None = None) -> None:
        self._provider = provider or MercadoLivreProvider()

    def search_products(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        return self._provider.search_products(query, limit=limit)

    def get_product(self, item_id: str) -> dict[str, Any]:
        return self._provider.get_product(item_id)

    def get_products_multiget(self, item_ids: list[str]) -> list[dict[str, Any]]:
        return self._provider.get_products_multiget(item_ids)

    def get_seller(self, seller_id: str) -> dict[str, Any]:
        return self._provider.get_seller(seller_id)

    def get_reviews(self, item_id: str) -> list[dict[str, Any]]:
        return self._provider.get_reviews(item_id)
