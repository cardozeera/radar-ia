"""Provider registry placeholder."""

from .base import BaseProvider


class ProviderRegistry:
    """Central registry for marketplace providers."""

    def __init__(self) -> None:
        self._providers: dict[str, BaseProvider] = {}

    def register(self, provider: BaseProvider) -> None:
        self._providers[provider.name] = provider

    def get(self, name: str) -> BaseProvider | None:
        return self._providers.get(name)
