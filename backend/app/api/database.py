"""Temporary database health endpoint."""

from fastapi import APIRouter, Depends

from ..services.database_service import DatabaseService

router = APIRouter(prefix="/health/database", tags=["health"])


def get_database_service() -> DatabaseService:
    return DatabaseService()


@router.get("")
def health_database(service: DatabaseService = Depends(get_database_service)) -> dict[str, object]:
    return service.health_check()
