"""Image resource routes."""

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel

from src.api.dependencies import get_civitai_service
from src.core.services.civitai_service import CivitaiService
from src.contracts.requests import GenerateImageRequest

router = APIRouter(prefix="/images", tags=["images"])


# Pydantic model for API validation (FastAPI requirement)
class CreateImageRequest(BaseModel):
    """Request to create a new image."""
    model: str
    prompt: str
    width: int = 512
    height: int = 512
    negative_prompt: str | None = None
    scheduler: str = "EulerA"
    steps: int = 20
    cfg_scale: float = 7.0
    seed: int | None = None
    clip_skip: int = 1
    timeout: int = 300
    return_image: bool = False


@router.post("")
async def create_image(
    request: CreateImageRequest,
    service: CivitaiService = Depends(get_civitai_service)
):
    """
    Create a new AI-generated image.

    If return_image=true, returns binary image data with metadata in headers.
    If return_image=false, returns JSON with blob URL and metadata.
    """
    try:
        # Convert to dataclass
        dto = GenerateImageRequest(
            model=request.model,
            prompt=request.prompt,
            width=request.width,
            height=request.height,
            negative_prompt=request.negative_prompt,
            scheduler=request.scheduler,
            steps=request.steps,
            cfg_scale=request.cfg_scale,
            seed=request.seed,
            clip_skip=request.clip_skip
        )

        # Generate and download image
        result = await service.generate_and_download(
            request=dto,
            timeout=request.timeout,
            poll_interval=3
        )

        # Return binary image or JSON based on flag
        if request.return_image:
            return Response(
                content=result['image_data'],
                media_type="image/png",
                headers={
                    "X-Seed": str(result['seed']),
                    "X-Cost": str(result.get('cost', 'N/A')),
                    "X-Job-ID": str(result.get('job_id', 'N/A'))
                }
            )
        else:
            return {
                "success": True,
                "job_id": result.get('job_id'),
                "seed": result['seed'],
                "cost": result.get('cost'),
                "blob_url": result['blob_url'],
                "prompt": result['prompt'],
                "model": result['model'],
                "message": f"Image generated successfully. Blob URL expires in 1 hour."
            }

    except TimeoutError as e:
        raise HTTPException(status_code=408, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
