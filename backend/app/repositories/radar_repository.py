"""Repository responsável pelo acesso aos dados dos radares no Supabase."""

from typing import Any
from uuid import UUID

from ..database.supabase import SupabaseClient
from ..models.radar import (
    Radar,
    RadarBrand,
    RadarKeyword,
    RadarOffer,
)


class RadarRepository:
    """Camada de persistência dos radares."""

    def __init__(self, client: SupabaseClient | None = None) -> None:
        self._client = client or SupabaseClient()
        self._db = self._client.get_client()

    def list_active(self) -> list[Radar]:
        """Retorna todos os radares ativos."""

        response = (
            self._db.table("radars")
            .select("*")
            .eq("active", True)
            .order("name")
            .execute()
        )

        return [
            Radar.model_validate(item)
            for item in (response.data or [])
        ]

    def get_by_slug(self, slug: str) -> Radar | None:
        """Busca um radar pelo slug."""

        response = (
            self._db.table("radars")
            .select("*")
            .eq("slug", slug)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return Radar.model_validate(response.data[0])

    def get_by_id(self, radar_id: UUID) -> Radar | None:
        """Busca um radar pelo ID."""

        response = (
            self._db.table("radars")
            .select("*")
            .eq("id", str(radar_id))
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return Radar.model_validate(response.data[0])

    def list_keywords(self, radar_id: UUID) -> list[RadarKeyword]:
        """Retorna as palavras-chave ativas de um radar."""

        response = (
            self._db.table("radar_keywords")
            .select("*")
            .eq("radar_id", str(radar_id))
            .eq("active", True)
            .order("priority")
            .execute()
        )

        return [
            RadarKeyword.model_validate(item)
            for item in (response.data or [])
        ]

    def list_brands(self, radar_id: UUID) -> list[RadarBrand]:
        """Retorna as marcas prioritárias de um radar."""

        response = (
            self._db.table("radar_brands")
            .select("*")
            .eq("radar_id", str(radar_id))
            .eq("active", True)
            .order("priority")
            .execute()
        )

        return [
            RadarBrand.model_validate(item)
            for item in (response.data or [])
        ]

    def save_offers(self, offers: list[RadarOffer]) -> int:
        """Salva ou atualiza ofertas classificadas."""

        if not offers:
            return 0

        rows: list[dict[str, Any]] = []

        for offer in offers:
            rows.append(
                {
                    "radar_id": str(offer.radar_id),
                    "provider": offer.provider,
                    "external_id": offer.external_id,
                    "title": offer.title,
                    "image_url": offer.image_url,
                    "permalink": offer.permalink,
                    "price": offer.price,
                    "original_price": offer.original_price,
                    "discount_percentage": offer.discount_percentage,
                    "rating": offer.rating,
                    "review_count": offer.review_count,
                    "sold_quantity": offer.sold_quantity,
                    "free_shipping": offer.free_shipping,
                    "seller_reputation": offer.seller_reputation,
                    "ranking_score": offer.ranking_score,
                    "ranking_explanation": offer.ranking_explanation,
                    "status": offer.status,
                }
            )

        response = (
            self._db.table("offers")
            .upsert(
                rows,
                on_conflict="radar_id,provider,external_id",
            )
            .execute()
        )

        return len(response.data or [])

    def list_top_offers(
        self,
        radar_id: UUID,
        limit: int = 5,
    ) -> list[RadarOffer]:
        """Retorna as melhores ofertas já salvas de um radar."""

        response = (
            self._db.table("offers")
            .select("*")
            .eq("radar_id", str(radar_id))
            .order("ranking_score", desc=True)
            .limit(limit)
            .execute()
        )

        rows = response.data or []
        offers: list[RadarOffer] = []

        radar = self.get_by_id(radar_id)

        if radar is None:
            return []

        for row in rows:
            offers.append(
                RadarOffer(
                    provider=row["provider"],
                    external_id=row["external_id"],
                    title=row["title"],
                    image_url=row.get("image_url"),
                    permalink=row["permalink"],
                    price=float(row.get("price") or 0),
                    original_price=(
                        float(row["original_price"])
                        if row.get("original_price") is not None
                        else None
                    ),
                    discount_percentage=row.get(
                        "discount_percentage",
                        0,
                    ),
                    rating=(
                        float(row["rating"])
                        if row.get("rating") is not None
                        else None
                    ),
                    review_count=row.get("review_count", 0),
                    sold_quantity=row.get("sold_quantity", 0),
                    free_shipping=row.get(
                        "free_shipping",
                        False,
                    ),
                    seller_reputation=row.get(
                        "seller_reputation"
                    ),
                    radar_id=radar_id,
                    radar_name=radar.name,
                    ranking_score=row.get(
                        "ranking_score",
                        0,
                    ),
                    ranking_explanation=row.get(
                        "ranking_explanation"
                    )
                    or "",
                    status=row.get("status", "pending"),
                    created_at=row.get("created_at"),
                    updated_at=row.get("updated_at"),
                )
            )

        return offers