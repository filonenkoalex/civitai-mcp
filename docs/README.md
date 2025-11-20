# Documentation Index

## Overview

Complete documentation for the Civitai MCP/API Server.

## Quick Links

### Getting Started
- [Main README](../README.md) - Project overview and setup
- [Project Structure](PROJECT_STRUCTURE.md) - Directory organization
- [Refactoring Summary](REFACTORING.md) - What was changed

### Architecture
- [Architecture Overview](architecture/PROPOSED_ARCHITECTURE.md)
- [Architecture Diagrams](architecture/DIAGRAMS.md)
- [Complete File Tree](architecture/FILE_TREE.md)

## Documentation Structure

```
docs/
├── README.md                    # This file
├── PROJECT_STRUCTURE.md         # Directory structure
├── REFACTORING.md              # Refactoring summary
└── architecture/
    ├── PROPOSED_ARCHITECTURE.md # Architecture details
    ├── DIAGRAMS.md             # Visual diagrams
    └── FILE_TREE.md            # Complete file tree
```

## For Developers

### Understanding the Codebase
1. Start with [Project Structure](PROJECT_STRUCTURE.md)
2. Review [Architecture Overview](architecture/PROPOSED_ARCHITECTURE.md)
3. See [Architecture Diagrams](architecture/DIAGRAMS.md)

### API Development
- API routes in `src/api/routes/`
- One file per resource
- See architecture docs for patterns

### MCP Development
- MCP tools in `src/mcp/tools/`
- One file per tool
- Follow SDK examples

### Core Services
- Business logic in `src/core/services/`
- Shared by both API and MCP
- Protocol-agnostic

## Running the Servers

```bash
# API Server
./scripts/run_api.sh

# MCP Server
./scripts/run_mcp.sh
```

## Contributing

See main [README](../README.md) for contribution guidelines.
