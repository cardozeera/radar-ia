"""Backward-compatible wrapper for the official FastAPI entrypoint."""

from app.main import app

__all__ = ["app"]
