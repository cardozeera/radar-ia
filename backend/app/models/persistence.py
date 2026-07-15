"""Pydantic models for persistence entities."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ProductRecord(BaseModel):
    id: str | None = None
    provider: str
    external_id: str
    title: str
    permalink: str | None = None
    image_url: str | None = None
    category_id: str | None = None
    seller_id: str | None = None
    seller_reputation: str | None = None
    rating: float | None = None
    review_count: int = 0
    sold_quantity: int = 0
    available_quantity: int = 0
    free_shipping: bool = False
    condition: str | None = None
    current_price: float | None = None
    original_price: float | None = None
    discount_percentage: int = 0
    score: int = 0
    score_breakdown: dict[str, Any] = Field(default_factory=dict)
    recommendation: str | None = None
    last_seen_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class WatchlistRecord(BaseModel):
    id: str | None = None
    provider: str = "mercadolivre"
    external_id: str
    title: str
    permalink: str
    image_url: str | None = None
    last_price: float | None = None
    last_checked_at: datetime | None = None
    active: bool = True
    created_at: datetime | None = None


class PriceHistoryRecord(BaseModel):
    id: str | None = None
    product_id: str
    price: float | None = None
    original_price: float | None = None
    discount_percentage: int = 0
    collected_at: datetime | None = None


class PublicationRecord(BaseModel):
    id: str | None = None
    product_external_id: str | None = None
    channel: str
    content: str
    affiliate_url: str | None = None
    status: str = "draft"
    created_at: datetime | None = None
    published_at: datetime | None = None


class SettingsRecord(BaseModel):
    key: str
    value: dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime | None = None
