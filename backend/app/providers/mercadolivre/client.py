"""Cliente da API do Mercado Livre com token salvo no Supabase."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import httpx

from ...database.supabase import SupabaseClient
from ..base import BaseProvider


class MercadoLivreProvider(BaseProvider):
    name = "mercadolivre"

    def __init__(
        self,
        base_url: str = "https://api.mercadolibre.com",
        timeout: int = 20,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._db = SupabaseClient().get_client()

    def search_products(
        self,
        query: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        payload = self._request(
            "/sites/MLB/search",
            params={
                "q": query,
                "limit": min(limit, 50),
            },
        )

        results = (
            payload.get("results", [])
            if isinstance(payload, dict)
            else []
        )

        offers: list[dict[str, Any]] = []

        for item in results[:limit]:
            try:
                detail = self.get_product(item.get("id"))
            except Exception:
                detail = self._normalize_product(item)

            offers.append(detail)

        return offers

    def get_product(self, external_id: str) -> dict[str, Any]:
        product_payload = self._request(
            f"/items/{external_id}"
        )

        reviews = self.get_reviews(external_id)

        seller = {}

        if product_payload.get("seller_id"):
            seller = self.get_seller(
                str(product_payload["seller_id"])
            )

        normalized = self._normalize_product(
            product_payload
        )

        normalized["reviews"] = reviews
        normalized["seller"] = seller

        return normalized

    def get_reviews(
        self,
        external_id: str,
    ) -> list[dict[str, Any]]:
        try:
            payload = self._request(
                f"/items/{external_id}/reviews"
            )
        except httpx.HTTPStatusError:
            return []

        if isinstance(payload, dict):
            reviews = payload.get("reviews")

            if isinstance(reviews, list):
                return reviews

        return []

    def get_seller(
        self,
        seller_id: str,
    ) -> dict[str, Any]:
        payload = self._request(
            f"/users/{seller_id}"
        )

        if not isinstance(payload, dict):
            return {}

        reputation = (
            payload.get("seller_reputation") or {}
        )

        return {
            "id": payload.get("id"),
            "nickname": payload.get("nickname"),
            "reputation": reputation,
            "status": payload.get("status"),
        }

    def _request(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        token = self._get_access_token()

        response = httpx.get(
            f"{self._base_url}{path}",
            params=params,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
            timeout=self._timeout,
        )

        if response.status_code == 401:
            token = self._refresh_access_token()

            response = httpx.get(
                f"{self._base_url}{path}",
                params=params,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
                timeout=self._timeout,
            )

        response.raise_for_status()

        return response.json()

    def _get_access_token(self) -> str:
        integration = self._get_integration()

        access_token = (
            integration.get("access_token") or ""
        ).strip()

        if not access_token:
            raise RuntimeError(
                "Access token do Mercado Livre não encontrado."
            )

        return access_token

    def _get_integration(self) -> dict[str, Any]:
        result = (
            self._db.table("integrations")
            .select("*")
            .eq("provider", "mercadolivre")
            .eq("active", True)
            .limit(1)
            .execute()
        )

        if not result.data:
            raise RuntimeError(
                "Integração do Mercado Livre não encontrada."
            )

        return result.data[0]

    def _refresh_access_token(self) -> str:
        integration = self._get_integration()

        refresh_token = (
            integration.get("refresh_token") or ""
        ).strip()

        client_id = os.getenv(
            "MELI_CLIENT_ID",
            "",
        ).strip()

        client_secret = os.getenv(
            "MELI_CLIENT_SECRET",
            "",
        ).strip()

        if not refresh_token:
            raise RuntimeError(
                "Refresh token do Mercado Livre não encontrado."
            )

        if not client_id or not client_secret:
            raise RuntimeError(
                "MELI_CLIENT_ID ou MELI_CLIENT_SECRET ausentes."
            )

        response = httpx.post(
            f"{self._base_url}/oauth/token",
            data={
                "grant_type": "refresh_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
            },
            headers={
                "Accept": "application/json",
                "Content-Type": (
                    "application/x-www-form-urlencoded"
                ),
            },
            timeout=self._timeout,
        )

        response.raise_for_status()

        token_data = response.json()

        access_token = (
            token_data.get("access_token") or ""
        ).strip()

        if not access_token:
            raise RuntimeError(
                "Mercado Livre não retornou novo access token."
            )

        self._db.table("integrations").update(
            {
                "access_token": access_token,
                "refresh_token": token_data.get(
                    "refresh_token",
                    refresh_token,
                ),
                "expires_in": token_data.get(
                    "expires_in"
                ),
                "updated_at": datetime.now(
                    timezone.utc
                ).isoformat(),
                "active": True,
            }
        ).eq(
            "provider",
            "mercadolivre",
        ).execute()

        return access_token

    def _normalize_product(
        self,
        item: dict[str, Any],
    ) -> dict[str, Any]:
        price = item.get("price")
        original_price = (
            item.get("original_price") or price
        )

        discount_percentage = item.get(
            "discount_percentage"
        )

        if (
            discount_percentage is None
            and original_price
            and price
            and float(original_price) > 0
        ):
            discount_percentage = int(
                round(
                    (
                        1
                        - (
                            float(price)
                            / float(original_price)
                        )
                    )
                    * 100
                )
            )

        discount_percentage = int(
            discount_percentage or 0
        )

        shipping = item.get("shipping") or {}
        seller = item.get("seller") or {}

        seller_reputation = (
            item.get("seller_reputation")
            or seller.get("power_seller_status")
            or ""
        )

        rating = item.get("rating")

        review_count = (
            item.get("review_count")
            or item.get("reviews")
            or 0
        )

        if isinstance(review_count, dict):
            review_count = (
                review_count.get("total") or 0
            )

        try:
            review_count = int(review_count)
        except (TypeError, ValueError):
            review_count = 0

        try:
            rating = (
                float(rating)
                if rating is not None
                else 0.0
            )
        except (TypeError, ValueError):
            rating = 0.0

        try:
            sold_quantity = int(
                item.get("sold_quantity") or 0
            )
        except (TypeError, ValueError):
            sold_quantity = 0

        return {
            "external_id": (
                item.get("id")
                or item.get("external_id")
            ),
            "imagem": (
                item.get("thumbnail")
                or item.get("secure_thumbnail")
                or item.get("image")
                or ""
            ),
            "titulo": (
                item.get("title")
                or item.get("name")
                or ""
            ),
            "preco": float(price or 0),
            "preco_original": float(
                original_price or price or 0
            ),
            "desconto": discount_percentage,
            "rating": rating,
            "avaliacoes": review_count,
            "vendidos": sold_quantity,
            "reputacao": seller_reputation,
            "frete_gratis": bool(
                shipping.get("free_shipping")
            ),
            "permalink_original": (
                item.get("permalink") or ""
            ),
            "seller_id": (
                seller.get("id")
                or item.get("seller_id")
            ),
        }