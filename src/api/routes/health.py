"""Health check routes."""

from fastapi import APIRouter
from dataclasses import asdict
from src.contracts.responses import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/")
async def root():
    """Root endpoint."""
    return asdict(HealthResponse(
        status="active",
        message="Civitai Image Generation API"
    ))


@router.get("/health")
async def health():
    """Health check."""
    return asdict(HealthResponse(status="healthy"))
