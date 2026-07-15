"""Converte o retorno do Mercado Livre em MarketplaceProduct."""

from ...models.radar import MarketplaceProduct


class MercadoLivreMapper:

    @staticmethod
    def to_product(item: dict) -> MarketplaceProduct:

        return MarketplaceProduct(

            provider="mercadolivre",

            external_id=item["external_id"],

            title=item["titulo"],

            image_url=item["imagem"],

            permalink=item["permalink_original"],

            price=item["preco"],

            original_price=item["preco_original"],

            discount_percentage=item["desconto"],

            rating=item["rating"],

            review_count=item["avaliacoes"],

            sold_quantity=item["vendidos"],

            free_shipping=item["frete_gratis"],

            seller_reputation=item["reputacao"],

            brand=item.get("brand"),

            raw_data=item,
        )