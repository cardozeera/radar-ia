"""Service for Supabase connectivity validation."""

from ..database.supabase import SupabaseClient


class DatabaseService:
    def __init__(self, client: SupabaseClient | None = None) -> None:
        self._client = client or SupabaseClient()

    def health_check(self) -> dict[str, object]:
        try:
            self._client.validate_configuration()
            client = self._client.get_client()
            client.table("products").select("id").limit(1).execute()
            return {"status": "ok", "database": "connected"}
        except Exception as exc:
            return {"status": "error", "database": "disconnected", "message": str(exc)}
