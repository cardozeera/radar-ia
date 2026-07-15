"""Base provider interface for marketplace integrations."""

from abc import ABC
from typing import Any


class BaseProvider(ABC):
    """Contract for marketplace providers."""

    name: str = "base"

    def search(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        return self.search_products(query, limit=limit)

    def search_products(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        raise NotImplementedError

    def get_product(self, external_id: str) -> dict[str, Any]:
        raise NotImplementedError

    def get_reviews(self, external_id: str) -> list[dict[str, Any]]:
        raise NotImplementedError

    def get_seller(self, seller_id: str) -> dict[str, Any]:
        raise NotImplementedError
