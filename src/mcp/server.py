"""MCP server setup for Civitai image generation."""

import base64
from mcp.server.fastmcp import FastMCP
from src.core.config.settings import settings
from src.core.services.civitai_service import CivitaiService
from src.contracts.requests import GenerateImageRequest

# Validate settings
settings.validate_token()

# Initialize service
service = CivitaiService(settings.civitai_api_token)

# Create FastMCP server
mcp = FastMCP("civitai-image-generator")


@mcp.tool()
async def generate_image(
    model: str,
    prompt: str,
    width: int = 512,
    height: int = 512,
    negative_prompt: str = None,
    steps: int = 20,
    cfg_scale: float = 7.0,
    seed: int = None,
    timeout: int = 300
) -> str:
    """Generate an AI image using Civitai.

    Args:
        model: Model URN (e.g., urn:air:sd1:checkpoint:civitai:4384@128713)
        prompt: Text description of the image to generate
        width: Image width in pixels
        height: Image height in pixels
        negative_prompt: Things to avoid in the image
        steps: Number of inference steps
        cfg_scale: Prompt adherence strength
        seed: Random seed for reproducibility
        timeout: Maximum wait time in seconds
    """
    # Create request
    request = GenerateImageRequest(
        model=model,
        prompt=prompt,
        width=width,
        height=height,
        negative_prompt=negative_prompt,
        steps=steps,
        cfg_scale=cfg_scale,
        seed=seed
    )

    # Generate and download image
    result = await service.generate_and_download(
        request=request,
        timeout=timeout,
        poll_interval=3
    )

    # Encode image as base64
    image_b64 = base64.b64encode(result['image_data']).decode('utf-8')

    # Return as data URI
    return f"data:image/png;base64,{image_b64}"
