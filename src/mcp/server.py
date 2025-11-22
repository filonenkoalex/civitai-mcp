"""MCP server setup for Civitai image generation."""

from mcp.server.fastmcp import FastMCP, Image

from src.contracts.requests import GenerateImageRequest
from src.core.config.settings import settings
from src.core.services.civitai_service import CivitaiService

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
    negative_prompt: str = "",
    steps: int = 20,
    cfg_scale: float = 7.0,
    seed: int = -1,
    timeout: int = 300,
) -> Image:
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
        seed=seed,
    )

    # Generate and download image
    result = await service.generate_and_download(
        request=request, timeout=timeout, poll_interval=3
    )

    # Extract format from content type (e.g., "image/png" -> "png", "image/jpeg" -> "jpeg")
    content_type = result.get("content_type", "image/png")
    image_format = content_type.split("/")[-1] if "/" in content_type else "png"

    # Return as Image object
    return Image(data=result["image_data"], format=image_format)
