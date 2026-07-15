"""Provider oficial do Mercado Livre."""

from ...models.radar import MarketplaceProduct
from .client import MercadoLivreProvider as MercadoLivreClient
from .mapper import MercadoLivreMapper


class MercadoLivreMarketplaceProvider:
    """Provider compatível com o Radar IA."""

    provider_name = "mercadolivre"

    def __init__(self):

        self.client = MercadoLivreClient()

    def search(
        self,
        keyword: str,
        limit: int = 10,
    ) -> list[MarketplaceProduct]:

        products = self.client.search_products(
            keyword,
            limit,
        )

        return [
            MercadoLivreMapper.to_product(item)
            for item in products
        ]