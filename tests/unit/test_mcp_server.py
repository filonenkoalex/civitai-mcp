"""Unit tests for MCP server."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.mcp.server import generate_image


class TestContentTypeFormatExtraction:
    """Test Content-Type header parsing for image format extraction."""

    @pytest.mark.asyncio
    async def test_format_extraction_simple(self):
        """Test simple Content-Type without parameters."""
        # Mock the service
        with patch("src.mcp.server.service") as mock_service:
            mock_service.generate_and_download = AsyncMock(
                return_value={
                    "image_data": b"fake_image_data",
                    "content_type": "image/png",
                    "seed": 123,
                }
            )

            result = await generate_image(
                model="urn:air:sd1:checkpoint:civitai:4384@128713",
                prompt="test prompt",
            )

            # Check that format is extracted correctly
            assert result.format == "png"

    @pytest.mark.asyncio
    async def test_format_extraction_with_charset(self):
        """Test Content-Type with charset parameter."""
        with patch("src.mcp.server.service") as mock_service:
            mock_service.generate_and_download = AsyncMock(
                return_value={
                    "image_data": b"fake_image_data",
                    "content_type": "image/jpeg; charset=utf-8",
                    "seed": 123,
                }
            )

            result = await generate_image(
                model="urn:air:sd1:checkpoint:civitai:4384@128713",
                prompt="test prompt",
            )

            # Should extract "jpeg", not "jpeg; charset=utf-8"
            assert result.format == "jpeg"

    @pytest.mark.asyncio
    async def test_format_extraction_with_multiple_parameters(self):
        """Test Content-Type with multiple parameters."""
        with patch("src.mcp.server.service") as mock_service:
            mock_service.generate_and_download = AsyncMock(
                return_value={
                    "image_data": b"fake_image_data",
                    "content_type": "image/webp; quality=80; charset=utf-8",
                    "seed": 123,
                }
            )

            result = await generate_image(
                model="urn:air:sd1:checkpoint:civitai:4384@128713",
                prompt="test prompt",
            )

            # Should extract "webp", ignoring all parameters
            assert result.format == "webp"

    @pytest.mark.asyncio
    async def test_format_extraction_with_spaces(self):
        """Test Content-Type with spaces around parameters."""
        with patch("src.mcp.server.service") as mock_service:
            mock_service.generate_and_download = AsyncMock(
                return_value={
                    "image_data": b"fake_image_data",
                    "content_type": "image/png ; charset=utf-8",
                    "seed": 123,
                }
            )

            result = await generate_image(
                model="urn:air:sd1:checkpoint:civitai:4384@128713",
                prompt="test prompt",
            )

            # Should handle spaces correctly
            assert result.format == "png"

    @pytest.mark.asyncio
    async def test_format_extraction_fallback(self):
        """Test fallback to png when Content-Type is missing."""
        with patch("src.mcp.server.service") as mock_service:
            mock_service.generate_and_download = AsyncMock(
                return_value={
                    "image_data": b"fake_image_data",
                    # No content_type key
                    "seed": 123,
                }
            )

            result = await generate_image(
                model="urn:air:sd1:checkpoint:civitai:4384@128713",
                prompt="test prompt",
            )

            # Should default to "png"
            assert result.format == "png"

    @pytest.mark.asyncio
    async def test_format_extraction_invalid_format(self):
        """Test with invalid Content-Type format."""
        with patch("src.mcp.server.service") as mock_service:
            mock_service.generate_and_download = AsyncMock(
                return_value={
                    "image_data": b"fake_image_data",
                    "content_type": "invalid/content/type",
                    "seed": 123,
                }
            )

            result = await generate_image(
                model="urn:air:sd1:checkpoint:civitai:4384@128713",
                prompt="test prompt",
            )

            # Should extract last part after "/"
            assert result.format == "type"


class TestGenerateImage:
    """Test the generate_image tool."""

    @pytest.mark.asyncio
    async def test_generate_image_basic(self):
        """Test basic image generation."""
        with patch("src.mcp.server.service") as mock_service:
            mock_service.generate_and_download = AsyncMock(
                return_value={
                    "image_data": b"fake_image_data",
                    "content_type": "image/png",
                    "seed": 42,
                    "job_id": "test_job_123",
                    "cost": 1.5,
                }
            )

            result = await generate_image(
                model="urn:air:sd1:checkpoint:civitai:4384@128713",
                prompt="a beautiful landscape",
                width=768,
                height=512,
            )

            # Verify the call was made with correct parameters
            call_args = mock_service.generate_and_download.call_args
            assert call_args[1]["timeout"] == 300
            assert call_args[1]["poll_interval"] == 3

            # Verify the request object
            request = call_args[1]["request"]
            assert request.model == "urn:air:sd1:checkpoint:civitai:4384@128713"
            assert request.prompt == "a beautiful landscape"
            assert request.width == 768
            assert request.height == 512

            # Verify result
            assert result.data == b"fake_image_data"
            assert result.format == "png"

    @pytest.mark.asyncio
    async def test_generate_image_with_all_params(self):
        """Test image generation with all parameters."""
        with patch("src.mcp.server.service") as mock_service:
            mock_service.generate_and_download = AsyncMock(
                return_value={
                    "image_data": b"fake_image_data",
                    "content_type": "image/jpeg",
                    "seed": 999,
                }
            )

            result = await generate_image(
                model="urn:air:sdxl:checkpoint:civitai:101055@128078",
                prompt="a futuristic city",
                width=1024,
                height=768,
                negative_prompt="blurry, bad quality",
                steps=30,
                cfg_scale=8.5,
                seed=999,
                timeout=600,
            )

            # Verify request parameters
            request = mock_service.generate_and_download.call_args[1]["request"]
            assert request.negative_prompt == "blurry, bad quality"
            assert request.steps == 30
            assert request.cfg_scale == 8.5
            assert request.seed == 999

            # Verify timeout was passed
            assert mock_service.generate_and_download.call_args[1]["timeout"] == 600

            # Verify result
            assert result.format == "jpeg"
