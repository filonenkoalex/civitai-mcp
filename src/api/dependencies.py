"""API dependencies."""

from functools import lru_cache
from src.core.services.civitai_service import CivitaiService
from src.core.config.settings import settings


@lru_cache
def get_civitai_service() -> CivitaiService:
    """Get Civitai service instance."""
    settings.validate_token()
    return CivitaiService(settings.civitai_api_token)
