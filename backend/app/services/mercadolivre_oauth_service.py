"""Serviço OAuth do Mercado Livre."""

from __future__ import annotations

import base64
import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import urlencode

import httpx

from ..database.supabase import SupabaseClient


class MercadoLivreOAuthService:
    """Gera autorização e troca o authorization code por tokens."""

    authorization_url = (
        "https://auth.mercadolivre.com.br/authorization"
    )
    token_url = "https://api.mercadolibre.com/oauth/token"

    def __init__(self) -> None:
        self.client_id = os.getenv(
            "MELI_CLIENT_ID",
            "",
        ).strip()

        self.client_secret = os.getenv(
            "MELI_CLIENT_SECRET",
            "",
        ).strip()

        self.redirect_uri = os.getenv(
            "MELI_REDIRECT_URI",
            "",
        ).strip()

        self._db = SupabaseClient().get_client()

    def validate_configuration(self) -> None:
        """Valida as configurações necessárias para o OAuth."""

        missing: list[str] = []

        if not self.client_id:
            missing.append("MELI_CLIENT_ID")

        if not self.client_secret:
            missing.append("MELI_CLIENT_SECRET")

        if not self.redirect_uri:
            missing.append("MELI_REDIRECT_URI")

        if missing:
            raise RuntimeError(
                "Configuração OAuth incompleta: "
                + ", ".join(missing)
            )

    def create_authorization_url(self) -> str:
        """Cria a URL de autorização com PKCE e state."""

        self.validate_configuration()

        state = secrets.token_urlsafe(32)
        code_verifier = secrets.token_urlsafe(64)

        digest = hashlib.sha256(
            code_verifier.encode("utf-8")
        ).digest()

        code_challenge = (
            base64.urlsafe_b64encode(digest)
            .decode("utf-8")
            .rstrip("=")
        )

        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(minutes=10)
        ).isoformat()

        self._db.table("oauth_states").insert(
            {
                "state": state,
                "code_verifier": code_verifier,
                "expires_at": expires_at,
            }
        ).execute()

        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }

        return (
            f"{self.authorization_url}?"
            f"{urlencode(params)}"
        )

    def exchange_code(
        self,
        code: str,
        state: str,
    ) -> dict[str, Any]:
        """Troca o authorization code pelos tokens."""

        self.validate_configuration()

        state_result = (
            self._db.table("oauth_states")
            .select("*")
            .eq("state", state)
            .limit(1)
            .execute()
        )

        if not state_result.data:
            raise RuntimeError(
                "State OAuth inválido ou já utilizado."
            )

        state_record = state_result.data[0]

        expires_at_raw = state_record.get("expires_at")

        if not expires_at_raw:
            self._delete_state(state)

            raise RuntimeError(
                "State OAuth sem data de validade."
            )

        expires_at = datetime.fromisoformat(
            expires_at_raw.replace("Z", "+00:00")
        )

        if expires_at < datetime.now(timezone.utc):
            self._delete_state(state)

            raise RuntimeError(
                "State OAuth expirado. Inicie a autorização novamente."
            )

        code_verifier = state_record.get("code_verifier")

        if not code_verifier:
            self._delete_state(state)

            raise RuntimeError(
                "Code verifier não encontrado."
            )

        try:
            response = httpx.post(
                self.token_url,
                data={
                    "grant_type": "authorization_code",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": self.redirect_uri,
                    "code_verifier": code_verifier,
                },
                headers={
                    "Accept": "application/json",
                    "Content-Type": (
                        "application/x-www-form-urlencoded"
                    ),
                },
                timeout=30,
            )
        except httpx.RequestError as exc:
            raise RuntimeError(
                "Falha de comunicação com o Mercado Livre."
            ) from exc

        if response.status_code >= 400:
            raise RuntimeError(
                "O Mercado Livre recusou a geração do token. "
                f"Status HTTP: {response.status_code}."
            )

        token_data = response.json()

        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in")
        user_id = token_data.get("user_id")

        if not access_token:
            raise RuntimeError(
                "O Mercado Livre não retornou um access token."
            )

        self._db.table("integrations").upsert(
            {
                "provider": "mercadolivre",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user_id": str(user_id or ""),
                "expires_in": expires_in,
                "active": True,
                "updated_at": datetime.now(
                    timezone.utc
                ).isoformat(),
            },
            on_conflict="provider",
        ).execute()

        self._delete_state(state)

        return {
            "status": "ok",
            "provider": "mercadolivre",
            "connected": True,
            "user_id": user_id,
            "expires_in": expires_in,
        }

    def _delete_state(self, state: str) -> None:
        """Remove um state utilizado, inválido ou expirado."""

        (
            self._db.table("oauth_states")
            .delete()
            .eq("state", state)
            .execute()
        )