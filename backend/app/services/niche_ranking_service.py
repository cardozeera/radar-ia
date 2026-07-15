"""Ranking engine for niche offers."""

import math
from dataclasses import dataclass
from ..models.niche import MarketplaceProduct

@dataclass(frozen=True)
class RankingResult:
    score: int
    explanation: str

class NicheRankingService:
    def calculate(self, product: MarketplaceProduct) -> RankingResult:
        rating = 0 if product.rating is None else round(max(0, min(1, (product.rating - 3.5) / 1.5)) * 30)
        reviews = self._volume(product.review_count, 20)
        sales = self._volume(product.sold_quantity, 25)
        discount = round(min(max(product.discount_percentage, 0), 40) / 40 * 15)
        shipping = 5 if product.free_shipping else 0
        seller = self._seller(product.seller_reputation)
        score = min(100, rating + reviews + sales + discount + shipping + seller)
        explanation = (
            f"Rating {product.rating or 0}; {product.review_count} avaliações; "
            f"{product.sold_quantity} vendidos; {product.discount_percentage}% de desconto; "
            f"{'frete grátis' if product.free_shipping else 'frete a consultar'}."
        )
        return RankingResult(score=score, explanation=explanation)

    @staticmethod
    def _volume(value: int, max_points: int) -> int:
        if value <= 0:
            return 0
        return round(min(1.0, math.log10(value + 1) / 4) * max_points)

    @staticmethod
    def _seller(value: str | None) -> int:
        text = (value or "").lower()
        if "platinum" in text:
            return 5
        if "gold" in text or "mercadolider" in text:
            return 4
        return 1 if text else 0
