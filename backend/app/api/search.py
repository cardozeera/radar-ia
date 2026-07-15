"""Search API routes without business logic or direct provider access."""

from fastapi import APIRouter, Depends

from ..models.schemas import ProviderSearchRequest, ProviderSearchResponse
from ..services.search_service import SearchService
from .dependencies import get_search_service

router = APIRouter(prefix="/api/search", tags=["search"])


@router.post("", response_model=ProviderSearchResponse)
def search_products(
    request: ProviderSearchRequest,
    service: SearchService = Depends(get_search_service),
) -> ProviderSearchResponse:
    return service.search(request)
