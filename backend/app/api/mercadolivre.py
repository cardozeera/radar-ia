"""Temporary Mercado Livre API routes."""

from fastapi import APIRouter, Depends, HTTPException, Query

from ..services.mercadolivre_service import MercadoLivreService
from .dependencies import get_mercadolivre_service

router = APIRouter(prefix="/api/mercadolivre", tags=["mercadolivre"])


@router.get("/search")
def search_products(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=20),
    service: MercadoLivreService = Depends(get_mercadolivre_service),
) -> dict[str, object]:
    try:
        results = service.search_products(q, limit=limit)
        return {"query": q, "count": len(results), "results": results}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

from typing import Any
from ..providers.mercadolivre.client import MercadoLivreProvider

@router.get("/me")
def me() -> dict[str, object]:
    provider = MercadoLivreProvider()
    user = provider.get_authenticated_user()

    return {
        "connected": True,
        "id": user.get("id"),
        "nickname": user.get("nickname"),
        "site_id": user.get("site_id"),
        "status": (user.get("status") or {}).get("site_status"),
    }