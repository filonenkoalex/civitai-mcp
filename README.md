# Civitai MCP/API Server

AI image generation service with both MCP and REST API interfaces.

## Overview

A clean, production-ready server providing two interfaces for Civitai's AI image generation:
- **MCP Server** - For Claude Desktop integration
- **REST API** - For direct HTTP access

Both share the same core business logic with proper separation of concerns.

## Features

✅ **Dual Interface** - MCP and REST API
✅ **Clean Architecture** - Layered design with clear boundaries
✅ **Type-Safe** - Dataclass DTOs with validation
✅ **Production Ready** - Error handling, logging, testing
✅ **Well Documented** - Comprehensive architecture docs

## Quick Start

### 1. Installation

\`\`\`bash
# Install dependencies
uv sync

# Create .env file
cat > .env << 'ENVEOF'
CIVITAI_API_TOKEN=your_token_here
ENVEOF
\`\`\`

Get your API token from: https://civitai.com/user/account

### 2. Run API Server

\`\`\`bash
./scripts/run_api.sh
# or
uv run python -m src.api.main
\`\`\`

Visit http://localhost:8000/docs for API documentation.

### 3. Run MCP Server

\`\`\`bash
./scripts/run_mcp.sh
# or
uv run python -m src.mcp.main
\`\`\`

## Architecture

\`\`\`
src/
├── api/          # FastAPI REST interface
├── mcp/          # MCP protocol interface
├── core/         # Shared business logic
├── contracts/    # Shared DTOs (@dataclass)
└── shared/       # Utilities
\`\`\`

### Key Principles

- **Separation of Concerns** - API, MCP, and Core are independent
- **Single Responsibility** - One file per tool/route
- **Shared Contracts** - Unified DTOs with @dataclass
- **Protocol Agnostic** - Core logic knows nothing about protocols

## Usage

### REST API

\`\`\`bash
# Generate image
curl -X POST http://localhost:8000/images/generate \\
  -H "Content-Type: application/json" \\
  -d '{
    "model": "urn:air:sd1:checkpoint:civitai:4384@128713",
    "prompt": "a serene mountain landscape",
    "width": 768,
    "height": 512
  }'

# Check job status
curl http://localhost:8000/jobs/{token}
\`\`\`

### MCP Tools

When configured in Claude Desktop:

- \`generate_image\` - Submit generation job
- \`check_job_status\` - Monitor progress
- \`generate_image_and_wait\` - Generate and wait for completion

## Configuration

### Environment Variables (.env)

\`\`\`env
CIVITAI_API_TOKEN=your_token_here
APP_HOST=0.0.0.0
APP_PORT=8000
\`\`\`

### Claude Desktop Config

Add to \`claude_desktop_config.json\`:

\`\`\`json
{
  "mcpServers": {
    "civitai": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/civitai-mcp-v2",
        "run",
        "python",
        "-m",
        "src.mcp.main"
      ],
      "env": {
        "CIVITAI_API_TOKEN": "your_token_here"
      }
    }
  }
}
\`\`\`

## Documentation

- [Project Structure](docs/PROJECT_STRUCTURE.md) - Directory organization
- [Architecture](docs/architecture/PROPOSED_ARCHITECTURE.md) - Design details
- [Diagrams](docs/architecture/DIAGRAMS.md) - Visual architecture
- [Refactoring](docs/REFACTORING.md) - What was changed

## Development

### Project Structure

\`\`\`
civitai-mcp-v2/
├── src/              # Source code
├── tests/            # Test suite
├── docs/             # Documentation
├── scripts/          # Run scripts
└── README.md         # This file
\`\`\`

### Adding Features

- **New API route** → Create file in \`src/api/routes/\`
- **New MCP tool** → Create file in \`src/mcp/tools/\`
- **New service** → Create file in \`src/core/services/\`

### Code Style

- Small, focused files (~50 lines average)
- Single responsibility per file
- Type hints everywhere
- Comprehensive docstrings

## Testing

\`\`\`bash
# Test API manually
curl http://localhost:8000/health
\`\`\`

## Popular Models

\`\`\`python
# Realistic Vision V6
"urn:air:sd1:checkpoint:civitai:4384@128713"

# DreamShaper XL
"urn:air:sdxl:checkpoint:civitai:101055@128078"
\`\`\`

Browse more at: https://civitai.com

## Support

- **Civitai API**: https://developer.civitai.com
- **MCP SDK**: https://github.com/modelcontextprotocol/python-sdk

## Changelog

### v0.3.0 (Current)
- ✨ Complete architecture refactor
- ✨ Unified contracts with @dataclass
- ✨ Simplified MCP tools
- ✨ Clean project structure
- ✨ Both API and MCP servers working

---

Built with ❤️ using FastAPI, MCP SDK, and Civitai API
