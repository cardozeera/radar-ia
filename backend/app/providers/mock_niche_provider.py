"""Temporary provider used before Mercado Livre OAuth."""

import hashlib
import random
from ..models.niche import MarketplaceProduct

class MockNicheProvider:
    provider_name = "mock"

    def search_products(self, query: str, limit: int = 10) -> list[MarketplaceProduct]:
        seed = int(hashlib.sha256(query.encode("utf-8")).hexdigest()[:8], 16)
        rng = random.Random(seed)
        products = []
        for index in range(limit):
            price = round(rng.uniform(49.9, 1999.9), 2)
            discount = rng.randint(5, 42)
            original_price = round(price / (1 - discount / 100), 2)
            products.append(MarketplaceProduct(
                provider=self.provider_name,
                external_id=f"MOCK-{seed}-{index}",
                title=f"{query.title()} — Oferta {index + 1}",
                image_url="https://placehold.co/600x400?text=Radar+IA",
                price=price,
                original_price=original_price,
                discount_percentage=discount,
                permalink="https://www.mercadolivre.com.br/",
                rating=round(rng.uniform(4.1, 5.0), 1),
                review_count=rng.randint(15, 2500),
                sold_quantity=rng.randint(8, 5000),
                free_shipping=rng.choice([True, True, False]),
                seller_reputation=rng.choice(["platinum", "gold", "mercadolider", "normal"]),
            ))
        return products
