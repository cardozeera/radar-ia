"""Repositories for niches, terms and offers."""

from typing import Any
from uuid import UUID
from ..database.supabase import SupabaseClient
from ..models.niche import Niche, NicheOffer, NicheSearchTerm

class NicheRepository:
    def __init__(self, client: SupabaseClient | None = None) -> None:
        self._db = (client or SupabaseClient()).get_client()

    def list_active(self) -> list[Niche]:
        result = self._db.table("niches").select("*").eq("active", True).order("name").execute()
        return [Niche.model_validate(row) for row in (result.data or [])]

    def get_by_slug(self, slug: str) -> Niche | None:
        result = self._db.table("niches").select("*").eq("slug", slug).limit(1).execute()
        return Niche.model_validate(result.data[0]) if result.data else None

class NicheSearchTermRepository:
    def __init__(self, client: SupabaseClient | None = None) -> None:
        self._db = (client or SupabaseClient()).get_client()

    def list_by_niche(self, niche_id: UUID) -> list[NicheSearchTerm]:
        result = self._db.table("niche_search_terms").select("*").eq("niche_id", str(niche_id)).eq("active", True).order("priority").execute()
        return [NicheSearchTerm.model_validate(row) for row in (result.data or [])]

class NicheOfferRepository:
    def __init__(self, client: SupabaseClient | None = None) -> None:
        self._db = (client or SupabaseClient()).get_client()

    def upsert_many(self, offers: list[NicheOffer]) -> None:
        rows: list[dict[str, Any]] = []
        for offer in offers:
            rows.append({
                "niche_id": str(offer.niche_id),
                "provider": offer.provider,
                "external_id": offer.external_id,
                "title": offer.title,
                "image_url": offer.image_url,
                "price": offer.price,
                "original_price": offer.original_price,
                "discount_percentage": offer.discount_percentage,
                "permalink": offer.permalink,
                "rating": offer.rating,
                "review_count": offer.review_count,
                "sold_quantity": offer.sold_quantity,
                "free_shipping": offer.free_shipping,
                "seller_reputation": offer.seller_reputation,
                "ranking_score": offer.ranking_score,
                "ranking_explanation": offer.ranking_explanation,
            })
        if rows:
            self._db.table("niche_offers").upsert(rows, on_conflict="niche_id,provider,external_id").execute()

    def list_top_by_niche(self, niche_id: UUID, limit: int = 5) -> list[dict[str, Any]]:
        result = self._db.table("niche_offers").select("*").eq("niche_id", str(niche_id)).order("ranking_score", desc=True).limit(limit).execute()
        return result.data or []
