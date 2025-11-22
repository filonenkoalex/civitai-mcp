#!/bin/bash
# Script to run MCP Inspector with the debug server
#
# Usage:
#   1. Start debugging in VS Code (F5 or Run > Start Debugging)
#   2. Run this script in a separate terminal
#   3. The inspector will connect to your debug session

cd "$(dirname "$0")/.." || exit

# Ensure API token is set
if [ -z "$CIVITAI_API_TOKEN" ]; then
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    else
        echo "Error: CIVITAI_API_TOKEN not set and no .env file found"
        exit 1
    fi
fi

echo "Starting MCP Inspector..."
echo "Make sure your MCP server is running in VS Code debugger first!"
echo ""

npx @modelcontextprotocol/inspector \
    uv --directory "$(pwd)" run python -m src.mcp.main

