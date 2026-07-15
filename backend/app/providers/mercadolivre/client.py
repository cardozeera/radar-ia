"""Mercado Livre provider backed by the public Mercado Livre API."""

from typing import Any

import httpx

from ..base import BaseProvider


class MercadoLivreProvider(BaseProvider):
    name = "mercadolivre"

    def __init__(self, base_url: str = "https://api.mercadolibre.com", timeout: int = 15) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def search_products(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        payload = self._request("/sites/MLB/search", params={"q": query, "limit": min(limit, 50)})
        results = payload.get("results", []) if isinstance(payload, dict) else []
        offers: list[dict[str, Any]] = []
        for item in results[:limit]:
            try:
                detail = self.get_product(item.get("id"))
            except Exception:
                detail = self._normalize_product(item)
            offers.append(detail)
        return offers

    def get_product(self, external_id: str) -> dict[str, Any]:
        product_payload = self._request(f"/items/{external_id}")
        reviews = self.get_reviews(external_id)
        seller = self.get_seller(product_payload.get("seller_id")) if product_payload.get("seller_id") else {}
        normalized = self._normalize_product(product_payload)
        normalized["reviews"] = reviews
        normalized["seller"] = seller
        return normalized

    def get_reviews(self, external_id: str) -> list[dict[str, Any]]:
        payload = self._request(f"/items/{external_id}/reviews")
        if isinstance(payload, dict):
            reviews = payload.get("reviews")
            if isinstance(reviews, list):
                return reviews
        return []

    def get_seller(self, seller_id: str) -> dict[str, Any]:
        payload = self._request(f"/users/{seller_id}")
        if not isinstance(payload, dict):
            return {}
        return {
            "id": payload.get("id"),
            "nickname": payload.get("nickname"),
            "reputation": payload.get("seller_reputation"),
            "status": payload.get("status"),
        }

    def _request(self, path: str, params: dict[str, Any] | None = None) -> Any:
        response = httpx.get(f"{self._base_url}{path}", params=params, timeout=self._timeout)
        response.raise_for_status()
        return response.json()

    def _normalize_product(self, item: dict[str, Any]) -> dict[str, Any]:
        price = item.get("price")
        original_price = item.get("original_price") or price
        discount_percentage = item.get("discount_percentage")
        if discount_percentage is None and original_price and price:
            if float(original_price) > 0:
                discount_percentage = int(round((1 - (float(price) / float(original_price))) * 100))
        if discount_percentage is None:
            discount_percentage = 0

        shipping = item.get("shipping") or {}
        seller = item.get("seller") or {}
        seller_reputation = item.get("seller_reputation") or seller.get("power_seller_status") or ""

        rating = item.get("rating")
        review_count = item.get("review_count") or item.get("reviews")
        if isinstance(review_count, dict):
            review_count = review_count.get("total")
        try:
            review_count = int(review_count or 0)
        except (TypeError, ValueError):
            review_count = 0

        if rating is None:
            rating = 0.0
        try:
            rating = float(rating)
        except (TypeError, ValueError):
            rating = 0.0

        sold_quantity = item.get("sold_quantity") or 0
        try:
            sold_quantity = int(sold_quantity)
        except (TypeError, ValueError):
            sold_quantity = 0

        return {
            "external_id": item.get("id") or item.get("external_id"),
            "imagem": item.get("thumbnail") or item.get("secure_thumbnail") or item.get("image") or "",
            "titulo": item.get("title") or item.get("name") or "",
            "preco": float(price or 0),
            "preco_original": float(original_price or price or 0),
            "desconto": int(discount_percentage or 0),
            "rating": rating,
            "avaliacoes": review_count,
            "vendidos": sold_quantity,
            "reputacao": seller_reputation,
            "frete_gratis": bool(shipping.get("free_shipping")),
            "permalink_original": item.get("permalink") or "",
            "seller_id": seller.get("id") or item.get("seller_id"),
        }
