"""Base repository abstraction."""

from abc import ABC, abstractmethod
from typing import Any


class BaseRepository(ABC):
    """Contract for persistence operations."""

    @abstractmethod
    def save(self, entity: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def list(self, *args: Any, **kwargs: Any) -> list[Any]:
        raise NotImplementedError
