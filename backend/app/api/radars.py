"""Rotas HTTP dos Radares."""

from fastapi import APIRouter, HTTPException

from ..models.radar import (
    Radar,
    RadarDetails,
    RadarOffersResponse,
)
from ..services.radar_service import RadarService

router = APIRouter(
    prefix="/api/radars",
    tags=["Radars"],
)

service = RadarService()


@router.get(
    "",
    response_model=list[Radar],
)
def list_radars():

    return service.list_radars()


@router.get(
    "/{slug}",
    response_model=RadarDetails,
)
def get_radar(
    slug: str,
):

    try:

        return service.get_radar(slug)

    except LookupError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.post(
    "/{slug}/run",
    response_model=RadarOffersResponse,
)
def run_radar(
    slug: str,
):

    try:

        return service.run(slug)

    except LookupError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.get(
    "/{slug}/offers",
    response_model=RadarOffersResponse,
)
def list_saved_offers(
    slug: str,
):

    try:

        return service.get_saved_offers(slug)

    except LookupError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )