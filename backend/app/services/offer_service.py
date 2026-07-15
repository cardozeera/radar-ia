"""Offer service placeholder."""

from .base import BaseService


class OfferService(BaseService):
    """Placeholder service that will orchestrate provider integrations later."""

    def run(self, *args, **kwargs):
        return {"status": "not_implemented"}
