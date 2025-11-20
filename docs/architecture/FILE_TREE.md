# Complete Project File Tree

## Overview
This is the complete file tree for the refactored Civitai MCP/API server.
All files are minimal, focused, and follow single responsibility principle.

## Full Structure

```
civitai-mcp-v2/
│
├── src/                                    # Source code root
│   │
│   ├── __init__.py                        # Package marker
│   │
│   ├── api/                                # FastAPI REST API
│   │   ├── __init__.py
│   │   ├── main.py                        # API server entry point (15 lines)
│   │   ├── dependencies.py                # Dependency injection (20 lines)
│   │   │
│   │   └── routes/                        # API routes (one per resource)
│   │       ├── __init__.py
│   │       ├── health.py                  # GET /health, GET / (10 lines)
│   │       ├── images.py                  # POST /images/generate (30 lines)
│   │       └── jobs.py                    # GET /jobs/{token} (25 lines)
│   │
│   ├── mcp/                                # MCP Server
│   │   ├── __init__.py
│   │   ├── main.py                        # MCP server entry point (10 lines)
│   │   ├── server.py                      # MCP server setup (30 lines)
│   │   │
│   │   └── tools/                         # MCP tools (one per tool)
│   │       ├── __init__.py                # Tool registry
│   │       ├── base.py                    # Base tool class (30 lines)
│   │       ├── generate_image.py          # Generate image tool (60 lines)
│   │       ├── check_job_status.py        # Check status tool (45 lines)
│   │       └── generate_and_wait.py       # Generate+wait tool (70 lines)
│   │
│   ├── core/                               # Core business logic (shared)
│   │   ├── __init__.py
│   │   │
│   │   ├── services/                      # Business services
│   │   │   ├── __init__.py
│   │   │   ├── base.py                    # Base service class (20 lines)
│   │   │   └── civitai_service.py         # Civitai API client (150 lines)
│   │   │
│   │   ├── models/                        # Domain models
│   │   │   ├── __init__.py
│   │   │   ├── image.py                   # Image model (30 lines)
│   │   │   ├── job.py                     # Job model (40 lines)
│   │   │   └── generation_params.py       # Generation parameters (50 lines)
│   │   │
│   │   └── config/                        # Configuration
│   │       ├── __init__.py
│   │       └── settings.py                # Settings management (40 lines)
│   │
│   ├── contracts/                          # Interface contracts (DTOs)
│   │   ├── __init__.py
│   │   │
│   │   ├── api/                           # API-specific DTOs
│   │   │   ├── __init__.py
│   │   │   ├── requests.py                # API request models (60 lines)
│   │   │   └── responses.py               # API response models (50 lines)
│   │   │
│   │   └── mcp/                           # MCP-specific DTOs
│   │       ├── __init__.py
│   │       └── responses.py               # MCP response models (40 lines)
│   │
│   └── shared/                             # Shared utilities
│       ├── __init__.py
│       ├── exceptions.py                  # Custom exceptions (30 lines)
│       ├── constants.py                   # Constants (20 lines)
│       └── validators.py                  # Common validators (40 lines)
│
├── configs/                                # Configuration files
│   ├── api.yaml                           # API server config
│   ├── mcp.yaml                           # MCP server config
│   └── models.yaml                        # Popular models reference
│
├── docs/                                   # Documentation
│   ├── README.md                          # Documentation index
│   │
│   ├── api/                               # API documentation
│   │   ├── README.md                      # API guide
│   │   ├── endpoints.md                   # Endpoint reference
│   │   └── examples.md                    # API examples
│   │
│   ├── mcp/                               # MCP documentation
│   │   ├── README.md                      # MCP guide
│   │   ├── tools.md                       # Tool reference
│   │   ├── setup.md                       # Claude Desktop setup
│   │   └── examples.md                    # MCP examples
│   │
│   └── architecture/                      # Architecture docs
│       ├── ARCHITECTURE.md                # Architecture overview
│       ├── DESIGN_PATTERNS.md             # Design patterns used
│       ├── DIAGRAMS.md                    # Architecture diagrams
│       └── FILE_TREE.md                   # This file
│
├── tests/                                  # Test suite
│   ├── __init__.py
│   ├── conftest.py                        # Pytest fixtures
│   │
│   ├── unit/                              # Unit tests
│   │   ├── __init__.py
│   │   ├── test_services/
│   │   │   ├── __init__.py
│   │   │   └── test_civitai_service.py
│   │   ├── test_models/
│   │   │   ├── __init__.py
│   │   │   └── test_generation_params.py
│   │   └── test_validators/
│   │       ├── __init__.py
│   │       └── test_validators.py
│   │
│   └── integration/                       # Integration tests
│       ├── __init__.py
│       ├── test_api/
│       │   ├── __init__.py
│       │   └── test_image_generation.py
│       └── test_mcp/
│           ├── __init__.py
│           └── test_tools.py
│
├── scripts/                                # Utility scripts
│   ├── run_api.sh                         # Run API server
│   ├── run_mcp.sh                         # Run MCP server
│   ├── test_service.sh                    # Test service layer
│   └── setup_env.sh                       # Environment setup
│
├── .env                                    # Environment variables (gitignored)
├── .env.example                           # Example environment file
├── .gitignore                             # Git ignore rules
├── pyproject.toml                         # Project configuration
├── README.md                              # Main readme
└── CHANGELOG.md                           # Version history
```

## File Count Summary

- **Source files:** 42 Python files
- **Config files:** 3 YAML files
- **Doc files:** 12 Markdown files
- **Scripts:** 4 Shell scripts
- **Test files:** 8 test files

**Total:** ~69 files (excluding __pycache__ and generated files)

## File Size Guidelines

- Entry points (main.py): 10-20 lines
- Tools/Routes: 30-70 lines
- Services: 100-200 lines
- Models: 20-50 lines
- DTOs: 40-60 lines
- Utilities: 20-40 lines

**Average file size:** ~50 lines
**Max file size:** 200 lines (civitai_service.py)

## Key Design Decisions

### 1. One Tool Per File
```
src/mcp/tools/
├── generate_image.py       # Single tool
├── check_job_status.py     # Single tool
└── generate_and_wait.py    # Single tool
```

### 2. One Route Group Per File
```
src/api/routes/
├── health.py               # Health endpoints
├── images.py               # Image endpoints
└── jobs.py                 # Job endpoints
```

### 3. Separate Contracts
```
src/contracts/
├── api/                    # API-specific DTOs
│   ├── requests.py
│   └── responses.py
└── mcp/                    # MCP-specific DTOs
    └── responses.py
```

### 4. Shared Core
```
src/core/
├── services/               # Business logic
├── models/                 # Domain models
└── config/                 # Configuration
```

## Import Patterns

### API Layer
```python
from src.core.services import CivitaiService
from src.contracts.api.requests import GenerateImageRequest
from src.contracts.api.responses import GenerateImageResponse
```

### MCP Layer
```python
from src.core.services import CivitaiService
from src.contracts.mcp.responses import ToolResponse
```

### Core Layer
```python
from src.core.models import Image, Job
from src.core.config import settings
```

## Entry Points

### API Server
```python
# src/api/main.py
from src.api.routes import health, images, jobs
app = FastAPI()
app.include_router(health.router)
app.include_router(images.router)
app.include_router(jobs.router)
```

### MCP Server
```python
# src/mcp/main.py
from src.mcp.server import create_server
server = create_server()
asyncio.run(server.run())
```

## Configuration Files

### configs/api.yaml
```yaml
server:
  host: 0.0.0.0
  port: 8000
  reload: true
cors:
  origins: ["*"]
```

### configs/mcp.yaml
```yaml
server:
  name: civitai-image-generator
  version: 0.3.0
tools:
  timeout: 300
```

### configs/models.yaml
```yaml
models:
  realistic_vision:
    urn: urn:air:sd1:checkpoint:civitai:4384@128713
    name: Realistic Vision V6.0
  dreamshaper_xl:
    urn: urn:air:sdxl:checkpoint:civitai:101055@128078
    name: DreamShaper XL
```

## Benefits of This Structure

### ✅ Clarity
- Obvious where each file belongs
- Clear separation of concerns
- Easy to navigate

### ✅ Maintainability
- Small, focused files
- Single responsibility
- Easy to modify

### ✅ Testability
- Clear test structure mirrors src/
- Easy to mock dependencies
- Isolated units

### ✅ Scalability
- Add new tools → new file in src/mcp/tools/
- Add new routes → new file in src/api/routes/
- Add new services → new file in src/core/services/

### ✅ Developer Experience
- Minimal files
- Clear naming
- Obvious locations
- No deep nesting

## Migration Strategy

1. **Phase 1:** Create directory structure
2. **Phase 2:** Move core layer (services, models, config)
3. **Phase 3:** Create contracts layer
4. **Phase 4:** Split MCP tools into separate files
5. **Phase 5:** Split API routes into separate files
6. **Phase 6:** Create entry points
7. **Phase 7:** Update documentation
8. **Phase 8:** Test everything

## Questions to Consider

1. **Is this structure clear?** ✓
2. **Are files small enough?** ✓ (avg 50 lines)
3. **Is separation of concerns obvious?** ✓
4. **Can we find files quickly?** ✓
5. **Is it easy to add new features?** ✓
6. **Will tests be easy to write?** ✓

## Ready to Proceed?

This structure follows:
- ✅ Clean Architecture principles
- ✅ SOLID principles
- ✅ Single Responsibility Principle
- ✅ Separation of Concerns
- ✅ Dependency Inversion
- ✅ Enterprise patterns

**Recommendation:** Proceed with implementation.
