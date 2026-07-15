"""Typed Pydantic models for API and domain boundaries."""

from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(default="ok")


class ProviderSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    provider: str = Field(default="mercadolivre")
    limit: int = Field(default=10, ge=1, le=50)


class ProviderSearchResponse(BaseModel):
    provider: str
    query: str
    results: list[dict[str, object]] = Field(default_factory=list)


class NicheDefinition(BaseModel):
    id: str
    name: str
    status: str = Field(default="active")
    keywords: list[str] = Field(default_factory=list)
    priority_brands: list[str] = Field(default_factory=list)
    min_discount: int = Field(default=0, ge=0, le=100)
    min_score: int = Field(default=0, ge=0, le=100)
    max_results: int = Field(default=10, ge=1, le=100)
    daily_publication_limit: int = Field(default=10, ge=0)


class NicheRunResponse(BaseModel):
    niche_id: str
    status: str
    result_count: int
    saved_count: int
    offers: list[dict[str, Any]] = Field(default_factory=list)
