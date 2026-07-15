"""Application service for niche radars."""

from ..models.niche import MarketplaceProduct, NicheDetails, NicheOffer, NicheOffersResponse
from ..providers.mock_niche_provider import MockNicheProvider
from ..repositories.niche_repository import NicheOfferRepository, NicheRepository, NicheSearchTermRepository
from .niche_ranking_service import NicheRankingService

class NicheService:
    def __init__(self) -> None:
        self._niches = NicheRepository()
        self._terms = NicheSearchTermRepository()
        self._offers = NicheOfferRepository()
        self._ranking = NicheRankingService()
        self._provider = MockNicheProvider()

    def list_niches(self):
        return self._niches.list_active()

    def get_details(self, slug: str) -> NicheDetails:
        niche = self._niches.get_by_slug(slug)
        if niche is None:
            raise LookupError(f"Nicho '{slug}' não encontrado.")
        return NicheDetails(niche=niche, search_terms=self._terms.list_by_niche(niche.id))

    def run(self, slug: str) -> NicheOffersResponse:
        details = self.get_details(slug)
        niche = details.niche
        collected: dict[str, MarketplaceProduct] = {}
        for term in details.search_terms:
            for product in self._provider.search_products(term.term, limit=10):
                collected[product.external_id] = product

        eligible = [
            p for p in collected.values()
            if (p.rating or 0) >= niche.minimum_rating
            and p.sold_quantity >= niche.minimum_sales
            and p.discount_percentage >= niche.minimum_discount
        ]

        ranked = []
        for product in eligible:
            result = self._ranking.calculate(product)
            ranked.append(NicheOffer(
                **product.model_dump(),
                niche_id=niche.id,
                niche_name=niche.name,
                ranking_score=result.score,
                ranking_explanation=result.explanation,
            ))

        ranked.sort(key=lambda p: (p.ranking_score, p.rating or 0, p.sold_quantity), reverse=True)
        top = ranked[: niche.result_limit]
        self._offers.upsert_many(top)
        return NicheOffersResponse(niche=niche.name, slug=niche.slug, count=len(top), results=top)

    def list_saved_offers(self, slug: str) -> NicheOffersResponse:
        niche = self._niches.get_by_slug(slug)
        if niche is None:
            raise LookupError(f"Nicho '{slug}' não encontrado.")
        rows = self._offers.list_top_by_niche(niche.id, niche.result_limit)
        results = [NicheOffer(
            provider=row["provider"],
            external_id=row["external_id"],
            title=row["title"],
            image_url=row.get("image_url"),
            price=float(row.get("price") or 0),
            original_price=float(row["original_price"]) if row.get("original_price") is not None else None,
            discount_percentage=row.get("discount_percentage", 0),
            permalink=row["permalink"],
            rating=float(row["rating"]) if row.get("rating") is not None else None,
            review_count=row.get("review_count", 0),
            sold_quantity=row.get("sold_quantity", 0),
            free_shipping=row.get("free_shipping", False),
            seller_reputation=row.get("seller_reputation"),
            niche_id=niche.id,
            niche_name=niche.name,
            ranking_score=row.get("ranking_score", 0),
            ranking_explanation=row.get("ranking_explanation") or "",
        ) for row in rows]
        return NicheOffersResponse(niche=niche.name, slug=niche.slug, count=len(results), results=results)
