"""Serviço responsável por calcular o ranking das ofertas."""

from dataclasses import dataclass
from math import log10

from ..models.radar import MarketplaceProduct


@dataclass(frozen=True)
class RankingResult:
    """Resultado do cálculo de ranking."""

    score: int
    explanation: str


class RadarRankingService:
    """Calcula uma nota de 0 a 100 para cada produto."""

    def calculate(self, product: MarketplaceProduct) -> RankingResult:
        rating_score = self._rating_score(product.rating)
        reviews_score = self._volume_score(
            product.review_count,
            maximum_points=20,
        )
        sales_score = self._volume_score(
            product.sold_quantity,
            maximum_points=25,
        )
        discount_score = self._discount_score(
            product.discount_percentage
        )
        shipping_score = 5 if product.free_shipping else 0
        seller_score = self._seller_score(
            product.seller_reputation
        )

        total_score = min(
            100,
            rating_score
            + reviews_score
            + sales_score
            + discount_score
            + shipping_score
            + seller_score,
        )

        explanation = self._build_explanation(
            product=product,
            rating_score=rating_score,
            reviews_score=reviews_score,
            sales_score=sales_score,
            discount_score=discount_score,
            shipping_score=shipping_score,
            seller_score=seller_score,
        )

        return RankingResult(
            score=total_score,
            explanation=explanation,
        )

    @staticmethod
    def _rating_score(rating: float | None) -> int:
        """
        Rating vale até 30 pontos.

        3.5 estrelas ou menos recebe zero.
        5 estrelas recebe 30.
        """

        if rating is None:
            return 0

        normalized = (rating - 3.5) / 1.5
        normalized = max(0.0, min(1.0, normalized))

        return round(normalized * 30)

    @staticmethod
    def _volume_score(
        value: int,
        maximum_points: int,
    ) -> int:
        """
        Usa escala logarítmica.

        Isso evita que produtos com milhares de vendas
        destruam completamente os demais produtos.
        """

        if value <= 0:
            return 0

        normalized = min(
            1.0,
            log10(value + 1) / 4,
        )

        return round(
            normalized * maximum_points
        )

    @staticmethod
    def _discount_score(
        discount_percentage: int,
    ) -> int:
        """
        Desconto vale até 15 pontos.

        Descontos de 40% ou mais recebem os 15 pontos.
        """

        discount = max(
            0,
            min(discount_percentage, 40),
        )

        return round(
            discount / 40 * 15
        )

    @staticmethod
    def _seller_score(
        seller_reputation: str | None,
    ) -> int:
        """Reputação do vendedor vale até 5 pontos."""

        reputation = (
            seller_reputation or ""
        ).strip().lower()

        if "platinum" in reputation:
            return 5

        if "gold" in reputation:
            return 4

        if "mercadolider" in reputation:
            return 4

        if "mercado líder" in reputation:
            return 4

        if reputation and reputation != "normal":
            return 2

        if reputation == "normal":
            return 1

        return 0

    @staticmethod
    def _build_explanation(
        product: MarketplaceProduct,
        rating_score: int,
        reviews_score: int,
        sales_score: int,
        discount_score: int,
        shipping_score: int,
        seller_score: int,
    ) -> str:
        """Cria uma explicação transparente da pontuação."""

        rating_text = (
            f"rating {product.rating:.1f}"
            if product.rating is not None
            else "sem rating informado"
        )

        shipping_text = (
            "frete grátis"
            if product.free_shipping
            else "frete a consultar"
        )

        seller_text = (
            product.seller_reputation
            or "reputação não informada"
        )

        return (
            f"{rating_text}; "
            f"{product.review_count} avaliações; "
            f"{product.sold_quantity} vendidos; "
            f"{product.discount_percentage}% de desconto; "
            f"{shipping_text}; "
            f"vendedor {seller_text}. "
            f"Pontuação: avaliação {rating_score}/30, "
            f"avaliações {reviews_score}/20, "
            f"vendas {sales_score}/25, "
            f"desconto {discount_score}/15, "
            f"frete {shipping_score}/5 e "
            f"vendedor {seller_score}/5."
        )