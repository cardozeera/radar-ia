"""Modelos de dados dos radares e ofertas."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class Radar(BaseModel):
    """Configuração principal de um radar."""

    id: UUID
    name: str
    slug: str
    description: str | None = None
    icon: str | None = None
    active: bool = True

    minimum_rating: float = 4.5
    minimum_sales: int = 10
    minimum_discount: int = 0
    result_limit: int = 5

    created_at: datetime | None = None
    updated_at: datetime | None = None


class RadarKeyword(BaseModel):
    """Palavra-chave monitorada por um radar."""

    id: UUID | None = None
    radar_id: UUID
    keyword: str
    priority: int = 1
    active: bool = True
    created_at: datetime | None = None


class RadarBrand(BaseModel):
    """Marca prioritária de um radar."""

    id: UUID | None = None
    radar_id: UUID
    brand: str
    priority: int = 1
    active: bool = True
    created_at: datetime | None = None


class MarketplaceProduct(BaseModel):
    """Produto normalizado recebido de um marketplace."""

    provider: str
    external_id: str
    title: str

    image_url: str | None = None
    permalink: str

    price: float = 0
    original_price: float | None = None
    discount_percentage: int = 0

    rating: float | None = None
    review_count: int = 0
    sold_quantity: int = 0

    free_shipping: bool = False
    seller_reputation: str | None = None
    brand: str | None = None

    raw_data: dict[str, Any] = Field(default_factory=dict)


class RadarOffer(MarketplaceProduct):
    """Oferta já classificada pelo Radar IA."""

    radar_id: UUID
    radar_name: str

    ranking_score: int
    ranking_explanation: str

    status: str = "pending"
    created_at: datetime | None = None
    updated_at: datetime | None = None


class RadarDetails(BaseModel):
    """Radar completo, incluindo palavras e marcas."""

    radar: Radar
    keywords: list[RadarKeyword]
    brands: list[RadarBrand]


class RadarOffersResponse(BaseModel):
    """Resposta dos Top 5 produtos de um radar."""

    radar: str
    slug: str
    count: int
    results: list[RadarOffer]