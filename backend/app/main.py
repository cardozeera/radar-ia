"""Application entrypoint for the Radar IA backend."""

from fastapi import FastAPI

from .api.router import router
from .core.settings import settings
from .database.supabase import SupabaseClient


def create_app() -> FastAPI:
    app = FastAPI(title="Radar IA", version="0.1.0")
    app.include_router(router)

    @app.on_event("startup")
    def validate_startup_configuration() -> None:
        client = SupabaseClient()
        app.state.supabase_configured = bool(settings.supabase_url and settings.supabase_secret_key)
        app.state.supabase_status = "configured" if app.state.supabase_configured else "not_configured"
        app.state.supabase_ping = client.ping()

    return app


app = create_app()
