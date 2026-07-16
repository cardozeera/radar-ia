"""Cliente da API do Mercado Livre com OAuth e diagnóstico detalhado."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import httpx

from ...database.supabase import SupabaseClient
from ..base import BaseProvider


class MercadoLivreProvider(BaseProvider):
    """Consulta e normaliza produtos da API do Mercado Livre."""

    name = "mercadolivre"

    def __init__(
        self,
        base_url: str = "https://api.mercadolibre.com",
        timeout: int = 20,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._db = SupabaseClient().get_client()

        self._base_headers = {
            "Accept": "application/json",
            "User-Agent": "RadarIA-App/1.0",
        }

    def search_products(
        self,
        query: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Busca produtos.

        Primeiro tenta a busca pública. Caso receba 401 ou 403,
        repete a chamada usando o access token salvo no Supabase.
        """

        safe_limit = max(1, min(limit, 50))

        payload = self._request(
            path="/sites/MLB/search",
            params={
                "q": query,
                "limit": safe_limit,
            },
            public_first=True,
        )

        results = (
            payload.get("results", [])
            if isinstance(payload, dict)
            else []
        )

        offers: list[dict[str, Any]] = []

        for item in results[:safe_limit]:
            external_id = item.get("id")

            if not external_id:
                continue

            try:
                product = self.get_product(
                    str(external_id)
                )
            except Exception:
                product = self._normalize_product(item)

            offers.append(product)

        return offers

    def get_product(
        self,
        external_id: str,
    ) -> dict[str, Any]:
        """Busca os detalhes de um anúncio."""

        product_payload = self._request(
            path=f"/items/{external_id}",
            public_first=True,
        )

        normalized = self._normalize_product(
            product_payload
        )

        reviews_payload = self.get_reviews(external_id)

        if reviews_payload:
            rating_average = reviews_payload.get(
                "rating_average"
            )

            paging = reviews_payload.get("paging") or {}

            if rating_average is not None:
                try:
                    normalized["rating"] = float(
                        rating_average
                    )
                except (TypeError, ValueError):
                    pass

            try:
                normalized["avaliacoes"] = int(
                    paging.get("total") or 0
                )
            except (TypeError, ValueError):
                normalized["avaliacoes"] = 0

            normalized["reviews"] = (
                reviews_payload.get("reviews") or []
            )
        else:
            normalized["reviews"] = []

        seller_id = product_payload.get("seller_id")

        if seller_id:
            try:
                seller = self.get_seller(
                    str(seller_id)
                )
            except Exception:
                seller = {}

            normalized["seller"] = seller

            reputation = seller.get(
                "power_seller_status"
            )

            if reputation:
                normalized["reputacao"] = reputation
        else:
            normalized["seller"] = {}

        return normalized

    def get_reviews(
        self,
        external_id: str,
    ) -> dict[str, Any]:
        """Busca avaliações do produto, quando disponíveis."""

        try:
            payload = self._request(
                path=f"/reviews/item/{external_id}",
                public_first=True,
            )
        except Exception:
            return {}

        return payload if isinstance(payload, dict) else {}

    def get_seller(
        self,
        seller_id: str,
    ) -> dict[str, Any]:
        """Busca informações públicas do vendedor."""

        payload = self._request(
            path=f"/users/{seller_id}",
            public_first=False,
        )

        if not isinstance(payload, dict):
            return {}

        reputation = (
            payload.get("seller_reputation") or {}
        )

        return {
            "id": payload.get("id"),
            "nickname": payload.get("nickname"),
            "status": payload.get("status"),
            "power_seller_status": reputation.get(
                "power_seller_status"
            ),
            "level_id": (
                reputation.get("transactions") or {}
            ).get("ratings"),
            "raw_reputation": reputation,
        }

    def _request(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        public_first: bool = False,
    ) -> Any:
        """
        Executa uma requisição.

        Para endpoints potencialmente públicos:
        1. tenta sem token;
        2. em 401/403, tenta autenticado.

        Para endpoints protegidos:
        1. usa token;
        2. em 401, renova e repete.
        """

        if public_first:
            response = self._send_get_request(
                path=path,
                params=params,
                token=None,
            )

            if response.status_code not in (401, 403):
                return self._parse_response(
                    response=response,
                    path=path,
                    request_mode="public",
                )

        token = self._get_access_token()

        response = self._send_get_request(
            path=path,
            params=params,
            token=token,
        )

        if response.status_code == 401:
            token = self._refresh_access_token()

            response = self._send_get_request(
                path=path,
                params=params,
                token=token,
            )

        return self._parse_response(
            response=response,
            path=path,
            request_mode="authenticated",
        )

    def _send_get_request(
        self,
        path: str,
        params: dict[str, Any] | None,
        token: str | None,
    ) -> httpx.Response:
        """Envia uma requisição GET para a API."""

        headers = self._base_headers.copy()

        if token:
            headers["Authorization"] = (
                f"Bearer {token}"
            )

        try:
            return httpx.get(
                f"{self._base_url}{path}",
                params=params,
                headers=headers,
                timeout=self._timeout,
                follow_redirects=True,
            )
        except httpx.RequestError as exc:
            raise RuntimeError(
                "Falha de comunicação com a API do "
                f"Mercado Livre em {path}: {exc}"
            ) from exc

    @staticmethod
    def _parse_response(
        response: httpx.Response,
        path: str,
        request_mode: str,
    ) -> Any:
        """Valida e converte a resposta da API."""

        if response.status_code >= 400:
            request_id = (
                response.headers.get("x-request-id")
                or response.headers.get(
                    "x-correlation-id"
                )
                or ""
            )

            raise RuntimeError(
                "Erro Mercado Livre: "
                f"status={response.status_code}; "
                f"mode={request_mode}; "
                f"path={path}; "
                f"request_id={request_id}; "
                f"response={response.text}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise RuntimeError(
                "O Mercado Livre retornou conteúdo "
                f"inválido em {path}."
            ) from exc

    def _get_integration(self) -> dict[str, Any]:
        """Obtém a integração ativa no Supabase."""

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
                "Integração ativa do Mercado Livre "
                "não encontrada no Supabase."
            )

        return result.data[0]

    def _get_access_token(self) -> str:
        """Obtém o access token atual."""

        integration = self._get_integration()

        access_token = str(
            integration.get("access_token") or ""
        ).strip()

        if not access_token:
            raise RuntimeError(
                "Access token do Mercado Livre "
                "não encontrado."
            )

        return access_token

    def _refresh_access_token(self) -> str:
        """Renova o access token usando o refresh token."""

        integration = self._get_integration()

        refresh_token = str(
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
                "Refresh token do Mercado Livre "
                "não encontrado."
            )

        if not client_id:
            raise RuntimeError(
                "MELI_CLIENT_ID não configurado."
            )

        if not client_secret:
            raise RuntimeError(
                "MELI_CLIENT_SECRET não configurado."
            )

        try:
            response = httpx.post(
                f"{self._base_url}/oauth/token",
                data={
                    "grant_type": "refresh_token",
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "refresh_token": refresh_token,
                },
                headers={
                    **self._base_headers,
                    "Content-Type": (
                        "application/"
                        "x-www-form-urlencoded"
                    ),
                },
                timeout=self._timeout,
            )
        except httpx.RequestError as exc:
            raise RuntimeError(
                "Falha de comunicação ao renovar "
                "o token do Mercado Livre."
            ) from exc

        if response.status_code >= 400:
            raise RuntimeError(
                "Erro ao renovar token do Mercado Livre: "
                f"status={response.status_code}; "
                f"response={response.text}"
            )

        try:
            token_data = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Resposta inválida ao renovar o token."
            ) from exc

        access_token = str(
            token_data.get("access_token") or ""
        ).strip()

        if not access_token:
            raise RuntimeError(
                "O Mercado Livre não retornou "
                "um novo access token."
            )

        new_refresh_token = str(
            token_data.get("refresh_token")
            or refresh_token
        ).strip()

        self._db.table("integrations").update(
            {
                "access_token": access_token,
                "refresh_token": new_refresh_token,
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

    @staticmethod
    def _normalize_product(
        item: dict[str, Any],
    ) -> dict[str, Any]:
        """Converte o produto para o formato do Radar IA."""

        price = item.get("price")

        original_price = (
            item.get("original_price") or price
        )

        discount_percentage = item.get(
            "discount_percentage"
        )

        try:
            price_float = float(price or 0)
        except (TypeError, ValueError):
            price_float = 0.0

        try:
            original_price_float = float(
                original_price or price or 0
            )
        except (TypeError, ValueError):
            original_price_float = price_float

        if (
            discount_percentage is None
            and original_price_float > 0
            and price_float >= 0
        ):
            discount_percentage = round(
                (
                    1
                    - (
                        price_float
                        / original_price_float
                    )
                )
                * 100
            )

        try:
            discount_percentage = max(
                0,
                int(discount_percentage or 0),
            )
        except (TypeError, ValueError):
            discount_percentage = 0

        shipping = item.get("shipping") or {}
        seller = item.get("seller") or {}

        seller_reputation = (
            item.get("seller_reputation")
            or seller.get("power_seller_status")
            or ""
        )

        if isinstance(seller_reputation, dict):
            seller_reputation = (
                seller_reputation.get(
                    "power_seller_status"
                )
                or ""
            )

        try:
            rating = float(
                item.get("rating") or 0
            )
        except (TypeError, ValueError):
            rating = 0.0

        review_count = (
            item.get("review_count")
            or item.get("reviews")
            or 0
        )

        if isinstance(review_count, dict):
            review_count = (
                review_count.get("total") or 0
            )

        if isinstance(review_count, list):
            review_count = len(review_count)

        try:
            review_count = int(review_count)
        except (TypeError, ValueError):
            review_count = 0

        try:
            sold_quantity = int(
                item.get("sold_quantity") or 0
            )
        except (TypeError, ValueError):
            sold_quantity = 0

        return {
            "external_id": str(
                item.get("id")
                or item.get("external_id")
                or ""
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
            "preco": price_float,
            "preco_original": original_price_float,
            "desconto": discount_percentage,
            "rating": rating,
            "avaliacoes": review_count,
            "vendidos": sold_quantity,
            "reputacao": str(
                seller_reputation or ""
            ),
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
            "brand": item.get("brand"),
        }
        def get_authenticated_user(self) -> dict[str, Any]:
    return self._request(
        path="/users/me",
        public_first=False,
    )