#!/bin/bash
# Run the MCP server

cd "$(dirname "$0")/.." || exit
uv run python -m src.mcp.main
