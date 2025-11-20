"""FastAPI server entry point."""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import health, images
from src.core.config.settings import settings


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title="Civitai Image Generation API",
        description="REST API for AI image generation using Civitai",
        version="0.3.0"
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    app.include_router(health.router)
    app.include_router(images.router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True
    )
