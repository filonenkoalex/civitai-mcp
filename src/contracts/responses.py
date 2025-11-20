"""Response DTOs using dataclasses."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class HealthResponse:
    """Health check response."""

    status: str = "healthy"
    message: Optional[str] = None
