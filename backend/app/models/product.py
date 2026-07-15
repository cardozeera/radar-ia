"""Product domain model placeholder."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Product:
    provider: str
    external_id: str
    title: str
    price: float
    currency: str = "BRL"
    metadata: dict[str, Any] = field(default_factory=dict)
