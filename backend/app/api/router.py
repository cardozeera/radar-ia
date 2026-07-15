"""API router aggregation."""

from fastapi import APIRouter

from .database import router as database_router
from .health import router as health_router
from .mercadolivre import router as mercadolivre_router
from .mercadolivre_oauth import router as mercadolivre_oauth_router
from .niches import router as niches_router
from .radars import router as radars_router
from .search import router as search_router

router = APIRouter()

router.include_router(health_router)
router.include_router(database_router)
router.include_router(search_router)

# legado
router.include_router(niches_router)

# nova arquitetura
router.include_router(radars_router)

# Mercado Livre
router.include_router(mercadolivre_router)
router.include_router(mercadolivre_oauth_router)