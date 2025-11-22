"""Civitai service for image generation operations."""

import asyncio
import os
import time
from typing import Any, Dict

from src.contracts.requests import GenerateImageRequest


class CivitaiService:
    """Service for interacting with Civitai API."""

    def __init__(self, api_token: str):
        """Initialize the service with API token."""
        self.api_token = api_token
        os.environ["CIVITAI_API_TOKEN"] = api_token
        self._civitai = None

    def _get_client(self):
        """Lazy load Civitai SDK."""
        if self._civitai is None:
            import civitai

            self._civitai = civitai.Civitai()
        return self._civitai

    async def generate_and_download(
        self, request: GenerateImageRequest, timeout: int = 300, poll_interval: int = 3
    ) -> Dict[str, Any]:
        """
        Generate an image and wait for completion, then download it.

        Args:
            request: Image generation parameters
            timeout: Maximum wait time in seconds
            poll_interval: Polling interval in seconds

        Returns:
            Dict with image_data (bytes), seed, and metadata
        """
        client = self._get_client()

        # Build input for Civitai API
        input_data = {
            "model": request.model,
            "params": {
                "prompt": request.prompt,
                "width": request.width,
                "height": request.height,
                "steps": request.steps,
                "cfgScale": request.cfg_scale,
                "clipSkip": request.clip_skip,
                "scheduler": request.scheduler,
            },
        }

        if request.negative_prompt:
            input_data["params"]["negativePrompt"] = request.negative_prompt
        if request.seed is not None:
            input_data["params"]["seed"] = request.seed

        # Submit job
        response = await client.image.create(input=input_data)

        if not isinstance(response, dict):
            raise ValueError("Unexpected response format from Civitai API")

        token = response.get("token")
        jobs = response.get("jobs", [])

        if not token:
            raise ValueError("No token received from Civitai API")

        job_id = jobs[0].get("jobId") if jobs else None
        cost = jobs[0].get("cost") if jobs else None

        # Wait for completion
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    f"Image generation did not complete within {timeout} seconds"
                )

            # Check status
            status_response = await client.jobs.get(token)

            if hasattr(status_response, "model_dump"):
                status_dict = status_response.model_dump()
            elif isinstance(status_response, dict):
                status_dict = status_response
            else:
                raise ValueError("Unexpected status response format")

            jobs_status = status_dict.get("jobs", [])
            if not jobs_status:
                await asyncio.sleep(poll_interval)
                continue

            job = jobs_status[0]
            result = job.get("result")

            if result and isinstance(result, list) and len(result) > 0:
                result_item = result[0]
                if result_item.get("available") and result_item.get("blobUrl"):
                    # Download the image
                    blob_url = result_item.get("blobUrl")
                    image_data, content_type = await self._download_image(blob_url)

                    return {
                        "image_data": image_data,
                        "content_type": content_type,
                        "seed": result_item.get("seed"),
                        "job_id": job_id,
                        "cost": cost,
                        "blob_url": blob_url,
                        "prompt": request.prompt,
                        "model": request.model,
                    }

            await asyncio.sleep(poll_interval)

    async def _download_image(self, blob_url: str) -> tuple[bytes, str]:
        """
        Download image from blob URL.

        Args:
            blob_url: URL to download from

        Returns:
            Tuple of (image data as bytes, content type)
        """
        import aiohttp

        async with aiohttp.ClientSession() as session:
            async with session.get(blob_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to download image: HTTP {response.status}")
                content_type = response.headers.get("Content-Type", "image/png")
                return await response.read(), content_type
