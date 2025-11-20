# Proposed Architecture - Civitai MCP/API Server

## Overview

Enterprise-grade architecture with clean separation between API and MCP layers, sharing core business logic.

## Directory Structure

```
civitai-mcp-v2/
├── src/                        # Source code root
│   ├── api/                    # FastAPI REST API layer
│   │   ├── __init__.py
│   │   ├── main.py            # API server entry point
│   │   ├── dependencies.py    # API dependency injection
│   │   └── routes/            # One file per endpoint group
│   │       ├── __init__.py
│   │       ├── health.py      # Health check endpoints
│   │       ├── images.py      # Image generation endpoints
│   │       └── jobs.py        # Job management endpoints
│   │
│   ├── mcp/                    # MCP Server layer
│   │   ├── __init__.py
│   │   ├── main.py            # MCP server entry point
│   │   ├── server.py          # MCP server setup
│   │   └── tools/             # One file per MCP tool
│   │       ├── __init__.py
│   │       ├── base.py        # Base tool class
│   │       ├── generate_image.py
│   │       ├── check_job_status.py
│   │       └── generate_and_wait.py
│   │
│   ├── core/                   # Core business logic (shared)
│   │   ├── __init__.py
│   │   ├── services/          # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── base.py        # Base service class
│   │   │   └── civitai_service.py
│   │   ├── models/            # Domain models
│   │   │   ├── __init__.py
│   │   │   ├── image.py
│   │   │   ├── job.py
│   │   │   └── generation_params.py
│   │   └── config/            # Configuration
│   │       ├── __init__.py
│   │       └── settings.py
│   │
│   ├── contracts/              # DTOs/Contracts (interface layer)
│   │   ├── __init__.py
│   │   ├── api/               # API-specific DTOs
│   │   │   ├── __init__.py
│   │   │   ├── requests.py    # API request models
│   │   │   └── responses.py   # API response models
│   │   └── mcp/               # MCP-specific DTOs
│   │       ├── __init__.py
│   │       └── responses.py   # MCP response models
│   │
│   └── shared/                 # Shared utilities
│       ├── __init__.py
│       ├── exceptions.py      # Custom exceptions
│       ├── constants.py       # Constants
│       └── validators.py      # Common validators
│
├── configs/                    # Configuration files
│   ├── api.yaml               # API server config
│   ├── mcp.yaml               # MCP server config
│   └── models.yaml            # Popular models reference
│
├── docs/                       # Documentation
│   ├── api/
│   │   ├── README.md          # API documentation
│   │   └── openapi.yaml       # OpenAPI spec
│   ├── mcp/
│   │   ├── README.md          # MCP documentation
│   │   └── tools.md           # Tool reference
│   └── architecture/
│       ├── ARCHITECTURE.md    # This file
│       ├── DESIGN_PATTERNS.md
│       └── DIAGRAMS.md
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── unit/                  # Unit tests
│   │   ├── test_services/
│   │   ├── test_models/
│   │   └── test_validators/
│   ├── integration/           # Integration tests
│   │   ├── test_api/
│   │   └── test_mcp/
│   └── conftest.py            # Pytest configuration
│
├── scripts/                    # Utility scripts
│   ├── run_api.sh             # Run API server
│   ├── run_mcp.sh             # Run MCP server
│   └── setup_env.sh           # Environment setup
│
├── .env.example               # Example environment file
├── .gitignore
├── pyproject.toml             # Project configuration
└── README.md                  # Main readme
```

## Architecture Principles

### 1. Separation of Concerns
- **API Layer** (`src/api/`) - HTTP/REST interface
- **MCP Layer** (`src/mcp/`) - MCP protocol interface
- **Core Layer** (`src/core/`) - Shared business logic
- **Contracts** (`src/contracts/`) - Interface definitions

### 2. Single Responsibility
- One file per route/tool
- One class per service
- One model per domain concept

### 3. Dependency Flow
```
API Layer  ─┐
            ├──> Core Layer (Services + Models)
MCP Layer  ─┘
```

### 4. Contract-Based Design
- API has its own request/response contracts
- MCP has its own response contracts
- Core layer uses domain models
- Clear boundaries between layers

## Layer Responsibilities

### API Layer (`src/api/`)
**Purpose:** HTTP REST interface for direct API access

**Responsibilities:**
- HTTP request/response handling
- API-specific validation
- OpenAPI documentation
- CORS, middleware, etc.
- Maps API contracts → Core models

**Does NOT:**
- Contain business logic
- Access Civitai API directly
- Know about MCP protocol

### MCP Layer (`src/mcp/`)
**Purpose:** MCP protocol interface for Claude Desktop

**Responsibilities:**
- MCP protocol handling
- Tool registration
- Stdio communication
- MCP-specific formatting
- Maps tool args → Core models

**Does NOT:**
- Contain business logic
- Access Civitai API directly
- Know about HTTP/REST

### Core Layer (`src/core/`)
**Purpose:** Business logic shared by all interfaces

**Responsibilities:**
- Civitai API integration
- Image generation logic
- Job management
- Domain models
- Configuration

**Does NOT:**
- Know about HTTP or MCP
- Handle protocol-specific concerns
- Format responses for specific interfaces

### Contracts Layer (`src/contracts/`)
**Purpose:** Define interface contracts (DTOs)

**Responsibilities:**
- API request/response schemas
- MCP response schemas
- Validation rules
- Documentation

**Does NOT:**
- Contain business logic
- Access external services

## File Organization Rules

### One Tool Per File (`src/mcp/tools/`)
```python
# generate_image.py
class GenerateImageTool:
    """Single MCP tool definition"""

    @property
    def definition(self) -> Tool:
        """Tool schema"""

    async def execute(self, args) -> list[TextContent]:
        """Tool execution"""
```

### One Route Group Per File (`src/api/routes/`)
```python
# images.py
router = APIRouter(prefix="/images", tags=["images"])

@router.post("/generate")
async def generate_image(...):
    """Single endpoint"""
```

### One Service Per File (`src/core/services/`)
```python
# civitai_service.py
class CivitaiService:
    """Single service class"""

    async def generate_image(...):
        """Business logic method"""
```

## Configuration Strategy

### configs/api.yaml
```yaml
server:
  host: 0.0.0.0
  port: 8000
  reload: true

cors:
  origins: ["*"]
  methods: ["*"]
```

### configs/mcp.yaml
```yaml
server:
  name: civitai-image-generator
  version: 0.2.0

tools:
  timeout: 300
  poll_interval: 3
```

## Entry Points

### API Server
```bash
# scripts/run_api.sh
uv run python -m src.api.main
```

### MCP Server
```bash
# scripts/run_mcp.sh
uv run python -m src.mcp.main
```

## Dependencies Between Modules

```
┌─────────────────────────────────────┐
│         API Layer / MCP Layer       │
│  (Routes/Tools - Protocol Specific) │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│         Contracts Layer             │
│    (DTOs - Interface Definitions)   │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│          Core Layer                 │
│   (Services - Business Logic)       │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│       External Services             │
│      (Civitai API, Storage)         │
└─────────────────────────────────────┘
```

## Benefits

### ✅ Maintainability
- Clear module boundaries
- Easy to locate code
- Single responsibility per file

### ✅ Testability
- Core logic isolated
- Easy to mock dependencies
- Clear test structure

### ✅ Scalability
- Add new routes without touching others
- Add new tools independently
- Core logic reusable

### ✅ Developer Experience
- Minimal files
- Clear naming conventions
- Obvious file locations

### ✅ Flexibility
- Can run API and MCP independently
- Can add new interfaces easily
- Business logic stays stable

## Migration Plan

1. Create new structure
2. Move core services
3. Split MCP tools into separate files
4. Split API routes into separate files
5. Create contract models
6. Update imports
7. Test both servers
8. Update documentation

## Success Criteria

- [ ] All files < 200 lines
- [ ] Each file has one clear purpose
- [ ] No circular dependencies
- [ ] Core layer has no protocol knowledge
- [ ] Both API and MCP servers run independently
- [ ] Full test coverage
- [ ] Clear documentation per layer
