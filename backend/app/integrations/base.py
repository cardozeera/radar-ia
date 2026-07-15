"""Base contract for external integrations."""

from abc import ABC, abstractmethod
from typing import Any


class BaseIntegration(ABC):
    """Contract for external services such as Supabase and provider APIs."""

    @abstractmethod
    def connect(self) -> Any:
        raise NotImplementedError
