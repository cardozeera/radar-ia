"""Base service abstractions placeholder."""

from abc import ABC, abstractmethod
from typing import Any


class BaseService(ABC):
    """Shared contract for future services."""

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
