"""Magalu provider placeholder."""

from ..base import BaseProvider


class MagaluProvider(BaseProvider):
    name = "magalu"

    def search(self, query: str, limit: int = 10) -> list[dict[str, object]]:
        return []
