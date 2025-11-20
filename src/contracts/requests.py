"""Request DTOs using dataclasses."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GenerateImageRequest:
    """Request to generate an image."""

    model: str
    prompt: str
    width: int = 512
    height: int = 512
    negative_prompt: Optional[str] = None
    scheduler: str = "EulerA"
    steps: int = 20
    cfg_scale: float = 7.0
    seed: Optional[int] = None
    clip_skip: int = 1
