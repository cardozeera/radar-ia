"""Shopee provider placeholder."""

from ..base import BaseProvider


class ShopeeProvider(BaseProvider):
    name = "shopee"

    def search(self, query: str, limit: int = 10) -> list[dict[str, object]]:
        return []
