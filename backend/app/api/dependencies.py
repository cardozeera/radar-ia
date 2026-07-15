"""FastAPI dependency wiring for application services."""

from ..core.settings import settings
from ..integrations.supabase_integration import SupabaseIntegration
from ..providers.amazon.client import AmazonProvider
from ..providers.magalu.client import MagaluProvider
from ..providers.mercadolivre.client import MercadoLivreProvider
from ..providers.registry import ProviderRegistry
from ..providers.shopee.client import ShopeeProvider
from ..providers.tiktokshop.client import TikTokShopProvider
from ..repositories.product_repository import ProductRepository
from ..repositories.watchlist_repository import WatchlistRepository
from ..services.mercadolivre_service import MercadoLivreService
from ..services.search_service import SearchService


def get_settings() -> object:
    return settings


def get_supabase_integration() -> SupabaseIntegration:
    return SupabaseIntegration(settings)


def get_provider_registry() -> ProviderRegistry:
    registry = ProviderRegistry()
    registry.register(MercadoLivreProvider())
    registry.register(AmazonProvider())
    registry.register(ShopeeProvider())
    registry.register(MagaluProvider())
    registry.register(TikTokShopProvider())
    return registry


def get_search_service() -> SearchService:
    return SearchService(get_provider_registry(), get_product_repository())


def get_mercadolivre_service() -> MercadoLivreService:
    return MercadoLivreService(MercadoLivreProvider())


def get_product_repository() -> ProductRepository:
    return ProductRepository(get_supabase_integration().connect())


def get_watchlist_repository() -> WatchlistRepository:
    return WatchlistRepository(get_supabase_integration().connect())
