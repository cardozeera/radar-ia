"""OAuth Mercado Livre."""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse

from ..services.mercadolivre_oauth_service import (
    MercadoLivreOAuthService,
)

router = APIRouter(
    prefix="/auth/mercadolivre",
    tags=["Mercado Livre OAuth"],
)

service = MercadoLivreOAuthService()


@router.get("/login")
def login():
    """
    Redireciona o usuário para a autorização do Mercado Livre.
    """
    try:
        url = service.create_authorization_url()
        return RedirectResponse(url=url)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.get("/callback")
def callback(
    code: str = Query(...),
    state: str = Query(...),
):
    """
    Recebe o callback do Mercado Livre.
    """

    try:
        return service.exchange_code(
            code=code,
            state=state,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )