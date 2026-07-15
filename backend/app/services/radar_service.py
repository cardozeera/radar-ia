"""Serviço principal do Radar IA."""

from __future__ import annotations

from ..models.radar import (
    MarketplaceProduct,
    RadarDetails,
    RadarOffer,
    RadarOffersResponse,
)
from ..providers.mercadolivre.mercadolivre_provider import (
    MercadoLivreMarketplaceProvider,
)
from ..repositories.radar_repository import RadarRepository
from .radar_ranking_service import RadarRankingService


class RadarService:
    """Coordena toda a execução de um Radar."""

    def __init__(self) -> None:

        self.repository = RadarRepository()

        # Agora usa o Mercado Livre real
        self.provider = MercadoLivreMarketplaceProvider()

        self.ranking = RadarRankingService()

    def list_radars(self):

        return self.repository.list_active()

    def get_radar(self, slug: str) -> RadarDetails:

        radar = self.repository.get_by_slug(slug)

        if radar is None:
            raise LookupError(f"Radar '{slug}' não encontrado.")

        return RadarDetails(
            radar=radar,
            keywords=self.repository.list_keywords(radar.id),
            brands=self.repository.list_brands(radar.id),
        )

    def run(self, slug: str) -> RadarOffersResponse:

        details = self.get_radar(slug)

        radar = details.radar

        collected: dict[str, MarketplaceProduct] = {}

        for keyword in details.keywords:

            products = self.provider.search(
                keyword.keyword,
                limit=10,
            )

            for product in products:
                collected[product.external_id] = product

        ranked: list[RadarOffer] = []

        for product in collected.values():

            if (product.rating or 0) < radar.minimum_rating:
                continue

            if product.sold_quantity < radar.minimum_sales:
                continue

            if product.discount_percentage < radar.minimum_discount:
                continue

            score = self.ranking.calculate(product)

            ranked.append(
                RadarOffer(
                    **product.model_dump(),
                    radar_id=radar.id,
                    radar_name=radar.name,
                    ranking_score=score.score,
                    ranking_explanation=score.explanation,
                )
            )

        ranked.sort(
            key=lambda x: (
                x.ranking_score,
                x.rating or 0,
                x.review_count,
                x.sold_quantity,
            ),
            reverse=True,
        )

        top = ranked[: radar.result_limit]

        self.repository.save_offers(top)

        return RadarOffersResponse(
            radar=radar.name,
            slug=radar.slug,
            count=len(top),
            results=top,
        )

    def get_saved_offers(
        self,
        slug: str,
    ) -> RadarOffersResponse:

        radar = self.repository.get_by_slug(slug)

        if radar is None:
            raise LookupError(
                f"Radar '{slug}' não encontrado."
            )

        offers = self.repository.list_top_offers(
            radar.id,
            radar.result_limit,
        )

        return RadarOffersResponse(
            radar=radar.name,
            slug=radar.slug,
            count=len(offers),
            results=offers,
        )