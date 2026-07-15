"""Mercado Livre health endpoint."""

from fastapi import APIRouter, Depends

from ..services.mercadolivre_service import MercadoLivreService
from .dependencies import get_mercadolivre_service

router = APIRouter(prefix="/health/mercadolivre", tags=["health"])


@router.get("")
def health_mercadolivre(service: MercadoLivreService = Depends(get_mercadolivre_service)) -> dict[str, object]:
    try:
        provider = service._provider
        token_configured = bool(getattr(provider, "_token", None))
        return {
            "status": "ok",
            "provider": "mercadolivre",
            "connected": token_configured,
        }
    except Exception as exc:
        return {"status": "error", "provider": "mercadolivre", "connected": False, "message": str(exc)}
