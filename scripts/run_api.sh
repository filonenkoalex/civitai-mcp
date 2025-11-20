#!/bin/bash
# Run the FastAPI server

cd "$(dirname "$0")/.." || exit
uv run python -m src.api.main
