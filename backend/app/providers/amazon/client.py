"""Amazon provider placeholder."""

from ..base import BaseProvider


class AmazonProvider(BaseProvider):
    name = "amazon"

    def search(self, query: str, limit: int = 10) -> list[dict[str, object]]:
        return []
