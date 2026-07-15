"""Mock Marketplace Provider.

Este provider simula um marketplace enquanto a integração
com o Mercado Livre ainda não está pronta.

Depois será substituído pelo MercadoLivreProvider,
sem alterar nenhuma outra parte do sistema.
"""

from __future__ import annotations

import random
from hashlib import md5

from ..models.radar import MarketplaceProduct


class MockMarketplaceProvider:
    """Provider temporário."""

    provider_name = "mock"

    def search(
        self,
        keyword: str,
        limit: int = 10,
    ) -> list[MarketplaceProduct]:

        # Faz os resultados serem sempre iguais
        seed = int(md5(keyword.encode()).hexdigest()[:8], 16)

        rng = random.Random(seed)

        products: list[MarketplaceProduct] = []

        for i in range(limit):

            price = round(
                rng.uniform(49.90, 1999.90),
                2,
            )

            discount = rng.randint(5, 40)

            original_price = round(
                price / (1 - discount / 100),
                2,
            )

            product = MarketplaceProduct(

                provider=self.provider_name,

                external_id=f"{seed}-{i}",

                title=f"{keyword.title()} #{i+1}",

                image_url="https://placehold.co/600x400?text=Radar+IA",

                permalink="https://mercadolivre.com.br",

                price=price,

                original_price=original_price,

                discount_percentage=discount,

                rating=round(
                    rng.uniform(4.1, 5.0),
                    1,
                ),

                review_count=rng.randint(
                    20,
                    3000,
                ),

                sold_quantity=rng.randint(
                    10,
                    8000,
                ),

                free_shipping=rng.choice(
                    [True, True, False]
                ),

                seller_reputation=rng.choice(
                    [
                        "platinum",
                        "gold",
                        "mercadolider",
                        "normal",
                    ]
                ),

                brand=rng.choice(
                    [
                        "Wilson",
                        "Head",
                        "Nike",
                        "Samsung",
                        "Apple",
                        "Mormaii",
                        "FCS",
                    ]
                ),

                raw_data={},
            )

            products.append(product)

        return products