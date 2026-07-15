"""HTTP routes for niche radars."""

from fastapi import APIRouter, HTTPException
from ..models.niche import Niche, NicheDetails, NicheOffersResponse
from ..services.niche_service import NicheService

router = APIRouter(prefix="/api/niches", tags=["niches"])

@router.get("", response_model=list[Niche])
def list_niches() -> list[Niche]:
    return NicheService().list_niches()

@router.get("/{slug}", response_model=NicheDetails)
def get_niche(slug: str) -> NicheDetails:
    try:
        return NicheService().get_details(slug)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@router.post("/{slug}/run", response_model=NicheOffersResponse)
def run_niche(slug: str) -> NicheOffersResponse:
    try:
        return NicheService().run(slug)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@router.get("/{slug}/offers", response_model=NicheOffersResponse)
def list_offers(slug: str) -> NicheOffersResponse:
    try:
        return NicheService().list_saved_offers(slug)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
