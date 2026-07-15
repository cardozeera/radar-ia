"""TikTok Shop provider placeholder."""

from ..base import BaseProvider


class TikTokShopProvider(BaseProvider):
    name = "tiktokshop"

    def search(self, query: str, limit: int = 10) -> list[dict[str, object]]:
        return []
