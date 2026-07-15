"""Pydantic models for niche radars."""

from datetime import datetime
from typing import Any
from uuid import UUID
from pydantic import BaseModel, Field

class Niche(BaseModel):
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

class NicheSearchTerm(BaseModel):
    id: UUID | None = None
    niche_id: UUID
    term: str
    priority: int = 1
    active: bool = True

class MarketplaceProduct(BaseModel):
    provider: str = "mock"
    external_id: str
    title: str
    image_url: str | None = None
    price: float = 0
    original_price: float | None = None
    discount_percentage: int = 0
    permalink: str
    rating: float | None = None
    review_count: int = 0
    sold_quantity: int = 0
    free_shipping: bool = False
    seller_reputation: str | None = None
    brand: str | None = None
    raw_data: dict[str, Any] = Field(default_factory=dict)

class NicheOffer(MarketplaceProduct):
    niche_id: UUID
    niche_name: str
    ranking_score: int
    ranking_explanation: str

class NicheDetails(BaseModel):
    niche: Niche
    search_terms: list[NicheSearchTerm]

class NicheOffersResponse(BaseModel):
    niche: str
    slug: str
    count: int
    results: list[NicheOffer]
