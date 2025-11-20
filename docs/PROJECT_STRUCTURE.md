# Project Structure - Civitai MCP/API Server

## Clean Project Structure

```
civitai-mcp-v2/
├── .env                        # Environment variables (gitignored)
├── .gitignore                  # Git ignore rules
├── README.md                   # Main project readme
├── REFACTORING_COMPLETE.md     # Refactoring summary
├── pyproject.toml              # Project configuration
├── uv.lock                     # Dependency lock file
│
├── src/                        # Source code
│   ├── api/                    # FastAPI REST API
│   │   ├── main.py             # API server entry point
│   │   ├── dependencies.py     # Dependency injection
│   │   └── routes/             # API routes (one per resource)
│   │       ├── health.py       # Health check endpoints
│   │       ├── images.py       # Image generation
│   │       └── jobs.py         # Job status
│   │
│   ├── mcp/                    # MCP Server
│   │   ├── main.py             # MCP server entry point
│   │   ├── server.py           # Server setup
│   │   └── tools/              # MCP tools (one per tool)
│   │       ├── generate_image.py
│   │       ├── check_job_status.py
│   │       └── generate_and_wait.py
│   │
│   ├── core/                   # Core business logic (shared)
│   │   ├── services/           # Business services
│   │   │   └── civitai_service.py
│   │   ├── models/             # Domain models
│   │   └── config/             # Configuration
│   │       └── settings.py
│   │
│   ├── contracts/              # Shared DTOs (@dataclass)
│   │   ├── requests.py         # Request DTOs
│   │   └── responses.py        # Response DTOs
│   │
│   └── shared/                 # Shared utilities
│
├── configs/                    # Configuration files
│
├── docs/                       # Documentation
│   └── architecture/           # Architecture documentation
│       ├── PROPOSED_ARCHITECTURE.md
│       ├── FILE_TREE.md
│       └── DIAGRAMS.md
│
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
│
└── scripts/                    # Utility scripts
    ├── run_api.sh              # Run API server
    └── run_mcp.sh              # Run MCP server
```

## Files Removed (moved to .remove/)

The following obsolete files were moved to `.remove/` folder:

### Old Implementation Files
- ❌ `main.py` - Old FastAPI server (replaced by `src/api/main.py`)
- ❌ `mcp_server.py` - Old MCP server (replaced by `src/mcp/main.py`)
- ❌ `config.py` - Old config (replaced by `src/core/config/settings.py`)
- ❌ `models.py` - Old Pydantic models (replaced by `src/contracts/`)
- ❌ `services/` - Old services directory (replaced by `src/core/services/`)

### Old Test Files
- ❌ `test_client.py` - Old API test client
- ❌ `test_service.py` - Old service test

### Old Documentation
- ❌ `MCP_CONVERSION_GUIDE.md` - Outdated
- ❌ `MCP_SERVER_README.md` - Outdated
- ❌ `QUICKSTART.md` - Outdated
- ❌ `QUICK_START.md` - Outdated
- ❌ `REFACTORING_SUMMARY.md` - Replaced by REFACTORING_COMPLETE.md

### Other
- ❌ `__pycache__/` - Python cache

## Active Files Count

- **Source files**: 15 Python files in `src/`
- **Config files**: Project configuration
- **Doc files**: Architecture documentation
- **Scripts**: 2 run scripts
- **Total**: Clean, minimal structure

## Key Principles

### ✅ What We Keep
- Active source code in `src/`
- Current documentation
- Configuration files
- Test structure
- Entry points

### ❌ What We Remove
- Duplicate implementations
- Outdated documentation
- Old test files
- Python cache
- Legacy code

## How to Use

### Run API Server
```bash
./scripts/run_api.sh
# or
uv run python -m src.api.main
```

### Run MCP Server
```bash
./scripts/run_mcp.sh
# or
uv run python -m src.mcp.main
```

### Install Dependencies
```bash
uv sync
```

## Benefits of Clean Structure

1. **Easy Navigation** - Everything has a clear place
2. **No Confusion** - No old/duplicate files
3. **Fast Onboarding** - New developers can understand quickly
4. **Maintainable** - Clear what's active vs archived
5. **Professional** - Enterprise-grade organization

## Archive Policy

- Old files are moved to `.remove/` (not deleted)
- `.remove/` is gitignored
- Can restore if needed
- Keep project root clean

## Success Metrics

- ✅ No duplicate files
- ✅ Clear directory structure
- ✅ All active code in `src/`
- ✅ Documentation up-to-date
- ✅ Old files archived, not mixed in
- ✅ Project root has <10 files
- ✅ Each file has clear purpose

The project is now **clean, organized, and ready for production**! 🎉
