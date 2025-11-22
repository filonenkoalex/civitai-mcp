#!/bin/bash
# Quick start script for debugging with MCP Inspector
# This script guides you through the debugging process

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🐛 MCP Debugging Quick Start"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Warning: .env file not found${NC}"
    echo "Creating .env file..."
    cat > .env << 'EOF'
CIVITAI_API_TOKEN=your_token_here
EOF
    echo -e "${YELLOW}Please edit .env and add your Civitai API token${NC}"
    echo "Get your token from: https://civitai.com/user/account"
    echo ""
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

if [ "$CIVITAI_API_TOKEN" = "your_token_here" ]; then
    echo -e "${YELLOW}⚠️  Please set your CIVITAI_API_TOKEN in .env${NC}"
    exit 1
fi

# Check if MCP Inspector is installed
if ! command -v npx &> /dev/null; then
    echo -e "${YELLOW}⚠️  npx not found. Please install Node.js first${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Debugging Steps:${NC}"
echo ""
echo "1️⃣  Open VS Code in this directory:"
echo "    code $PROJECT_ROOT"
echo ""
echo "2️⃣  Set breakpoints in VS Code:"
echo "    • Open: src/mcp/server.py"
echo "    • Click left of line 45 (request creation)"
echo "    • Click left of line 57 (API call)"
echo ""
echo "3️⃣  Start debugging in VS Code:"
echo "    • Press F5 (or Run > Start Debugging)"
echo "    • Select: 'Debug MCP Server (Direct)'"
echo ""
echo "4️⃣  Once debugging starts, come back and press Enter here..."
read -p "" 

echo ""
echo -e "${GREEN}✅ Starting MCP Inspector...${NC}"
echo ""
echo "The inspector will open in your browser."
echo "You'll see your 'generate_image' tool."
echo ""
echo -e "${BLUE}📝 Test Case (copy this):${NC}"
echo ""
cat << 'EOF'
{
  "model": "urn:air:sd1:checkpoint:civitai:4384@128713",
  "prompt": "a serene mountain landscape at sunset",
  "width": 512,
  "height": 512
}
EOF
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run the inspector
npx @modelcontextprotocol/inspector \
    uv --directory "$PROJECT_ROOT" run python -m src.mcp.main

