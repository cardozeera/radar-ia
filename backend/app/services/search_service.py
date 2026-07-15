"""Application service for provider-backed searches and niche radar execution."""

from datetime import datetime, timezone
from typing import Any

from ..models.persistence import ProductRecord
from ..models.schemas import NicheDefinition, NicheRunResponse, ProviderSearchRequest, ProviderSearchResponse
from ..providers.registry import ProviderRegistry
from ..repositories.product_repository import ProductRepository


class SearchService:
    """Business service responsible for orchestrating provider access."""

    def __init__(self, registry: ProviderRegistry, product_repository: ProductRepository | None = None) -> None:
        self._registry = registry
        self._product_repository = product_repository or ProductRepository()
        self._niche_runs: dict[str, list[dict[str, Any]]] = {}

    def search(self, request: ProviderSearchRequest) -> ProviderSearchResponse:
        provider = self._registry.get(request.provider)
        if provider is None:
            raise ValueError(f"Provider not registered: {request.provider}")

        results = provider.search(request.query, request.limit)
        return ProviderSearchResponse(
            provider=request.provider,
            query=request.query,
            results=results,
        )

    def list_niches(self) -> list[NicheDefinition]:
        return self._default_niches()

    def get_niche(self, niche_id: str) -> NicheDefinition | None:
        for niche in self._default_niches():
            if niche.id == niche_id:
                return niche
        return None

    def run_niche(self, niche_id: str) -> NicheRunResponse:
        niche = self.get_niche(niche_id)
        if niche is None:
            raise ValueError(f"Nicho não encontrado: {niche_id}")

        provider = self._registry.get("mercadolivre")
        if provider is None:
            raise ValueError("Provider Mercado Livre não está registrado")

        offers: list[dict[str, Any]] = []
        seen_ids: set[str] = set()

        for keyword in niche.keywords:
            try:
                results = provider.search_products(keyword, limit=max(5, niche.max_results))
            except Exception:
                continue

            for result in results:
                normalized = self._normalize_offer(result, niche)
                if normalized is None:
                    continue
                if normalized["external_id"] in seen_ids:
                    continue
                seen_ids.add(normalized["external_id"])
                offers.append(normalized)

        offers = sorted(offers, key=lambda item: item["score"], reverse=True)[: niche.max_results]
        saved_count = 0
        for offer in offers:
            try:
                self._product_repository.upsert_product(self._build_product_record(offer))
                saved_count += 1
            except Exception:
                continue

        self._niche_runs[niche_id] = offers
        return NicheRunResponse(
            niche_id=niche_id,
            status="completed",
            result_count=len(offers),
            saved_count=saved_count,
            offers=offers,
        )

    def get_niche_offers(self, niche_id: str) -> list[dict[str, Any]]:
        if niche_id in self._niche_runs:
            return self._niche_runs[niche_id]
        return []

    def get_product_detail(self, external_id: str) -> dict[str, Any]:
        provider = self._registry.get("mercadolivre")
        if provider is None:
            raise ValueError("Provider Mercado Livre não está registrado")
        product = provider.get_product(external_id)
        return self._normalize_offer(product)

    def _normalize_offer(self, offer: dict[str, Any], niche: NicheDefinition | None = None) -> dict[str, Any] | None:
        external_id = offer.get("external_id") or offer.get("id")
        if not external_id:
            return None

        price = float(offer.get("preco") or 0)
        original_price = float(offer.get("preco_original") or price or 0)
        discount = int(offer.get("desconto") or 0)
        rating = float(offer.get("rating") or 0)
        review_count = int(offer.get("avaliacoes") or 0)
        sold_quantity = int(offer.get("vendidos") or 0)
        seller_reputation = offer.get("reputacao") or ""
        free_shipping = bool(offer.get("frete_gratis"))

        score, breakdown = self._calculate_radar_score(
            discount=discount,
            rating=rating,
            review_count=review_count,
            sold_quantity=sold_quantity,
            seller_reputation=seller_reputation,
            free_shipping=free_shipping,
        )

        if niche is not None and (score < niche.min_score or discount < niche.min_discount):
            return None

        explanation = (
            f"Desconto {discount}% | Rating {rating:.1f} | Avaliações {review_count} | Vendidos {sold_quantity} | "
            f"Reputação {seller_reputation or 'não informada'} | Frete grátis {'sim' if free_shipping else 'não'}"
        )

        return {
            "external_id": str(external_id),
            "imagem": offer.get("imagem") or "",
            "titulo": offer.get("titulo") or "",
            "preco": price,
            "preco_original": original_price,
            "desconto": discount,
            "rating": round(rating, 2),
            "avaliacoes": review_count,
            "vendidos": sold_quantity,
            "reputacao": seller_reputation,
            "frete_gratis": free_shipping,
            "permalink_original": offer.get("permalink_original") or "",
            "score": score,
            "explicacao": explanation,
            "score_breakdown": breakdown,
        }

    def _calculate_radar_score(
        self,
        *,
        discount: int,
        rating: float,
        review_count: int,
        sold_quantity: int,
        seller_reputation: str,
        free_shipping: bool,
    ) -> tuple[int, dict[str, Any]]:
        discount_score = min(discount, 30)
        rating_score = min(int(rating * 6), 25)
        review_score = min(int(review_count / 20), 15)
        sold_score = min(int(sold_quantity / 200), 15)
        reputation_score = self._reputation_score(seller_reputation)
        shipping_score = 10 if free_shipping else 0
        total = round(discount_score + rating_score + review_score + sold_score + reputation_score + shipping_score)

        breakdown = {
            "desconto": discount_score,
            "rating": rating_score,
            "avaliacoes": review_score,
            "vendidos": sold_score,
            "reputacao": reputation_score,
            "frete_gratis": shipping_score,
        }
        return total, breakdown

    def _reputation_score(self, seller_reputation: str) -> int:
        if not seller_reputation:
            return 0
        normalized = seller_reputation.lower()
        if normalized in {"excellent", "high", "top", "melhor"}:
            return 15
        if normalized in {"good", "average", "medio", "regular"}:
            return 8
        return 5

    def _build_product_record(self, offer: dict[str, Any]) -> ProductRecord:
        return ProductRecord(
            provider="mercadolivre",
            external_id=offer["external_id"],
            title=offer["titulo"],
            permalink=offer.get("permalink_original"),
            image_url=offer.get("imagem"),
            seller_reputation=offer.get("reputacao"),
            rating=offer.get("rating"),
            review_count=offer.get("avaliacoes", 0),
            sold_quantity=offer.get("vendidos", 0),
            free_shipping=bool(offer.get("frete_gratis")),
            current_price=offer.get("preco"),
            original_price=offer.get("preco_original"),
            discount_percentage=offer.get("desconto", 0),
            score=offer.get("score", 0),
            score_breakdown=offer.get("score_breakdown", {}),
            recommendation=offer.get("explicacao"),
            last_seen_at=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    def _default_niches(self) -> list[NicheDefinition]:
        return [
            NicheDefinition(
                id="tenis",
                name="Tênis",
                status="active",
                keywords=["tenis masculino", "tenis casual", "tenis running"],
                priority_brands=["Nike", "Adidas", "Puma"],
                min_discount=10,
                min_score=55,
                max_results=10,
                daily_publication_limit=5,
            ),
            NicheDefinition(
                id="ferramentas",
                name="Ferramentas",
                status="active",
                keywords=["ferramenta profissional", "kit de ferramentas", "chave de fenda"],
                priority_brands=["Black+Decker", "Stanley", "DeWalt"],
                min_discount=8,
                min_score=50,
                max_results=10,
                daily_publication_limit=5,
            ),
            NicheDefinition(
                id="tecnologia",
                name="Tecnologia",
                status="active",
                keywords=["headset bluetooth", "smartwatch", "carregador usb"],
                priority_brands=["Samsung", "Apple", "Xiaomi"],
                min_discount=12,
                min_score=60,
                max_results=10,
                daily_publication_limit=5,
            ),
        ]
