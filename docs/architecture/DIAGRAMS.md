# Architecture Diagrams

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                              │
│  ┌──────────────────┐              ┌──────────────────┐         │
│  │  HTTP Clients    │              │ Claude Desktop   │         │
│  │  (curl, browser) │              │  (MCP Client)    │         │
│  └────────┬─────────┘              └─────────┬────────┘         │
└───────────┼────────────────────────────────┼──────────────────┘
            │                                  │
            │ HTTP/REST                        │ MCP/stdio
            │                                  │
┌───────────▼──────────────────────────────────▼──────────────────┐
│                     Interface Layer                              │
│  ┌─────────────────────┐          ┌────────────────────┐        │
│  │   API Routes        │          │    MCP Tools       │        │
│  │   src/api/routes/   │          │   src/mcp/tools/   │        │
│  │  ┌──────────────┐   │          │  ┌──────────────┐  │        │
│  │  │ health.py    │   │          │  │ generate_    │  │        │
│  │  │ images.py    │   │          │  │   image.py   │  │        │
│  │  │ jobs.py      │   │          │  │ check_job_   │  │        │
│  │  └──────────────┘   │          │  │   status.py  │  │        │
│  └──────────┬──────────┘          │  │ generate_    │  │        │
│             │                      │  │   and_wait.py│  │        │
│             │                      │  └──────────────┘  │        │
│             │                      └────────┬───────────┘        │
└─────────────┼────────────────────────────────┼──────────────────┘
              │                                │
              │ Uses contracts                 │ Uses contracts
              │                                │
┌─────────────▼────────────────────────────────▼──────────────────┐
│                     Contracts Layer                              │
│  ┌──────────────────────┐        ┌─────────────────────┐        │
│  │   API Contracts      │        │   MCP Contracts     │        │
│  │ src/contracts/api/   │        │ src/contracts/mcp/  │        │
│  │  ┌────────────────┐  │        │  ┌───────────────┐  │        │
│  │  │ requests.py    │  │        │  │ responses.py  │  │        │
│  │  │ responses.py   │  │        │  └───────────────┘  │        │
│  │  └────────────────┘  │        │                     │        │
│  └──────────┬───────────┘        └──────────┬──────────┘        │
└─────────────┼────────────────────────────────┼──────────────────┘
              │                                │
              └────────────┬───────────────────┘
                           │ Maps to/from
                           │
┌──────────────────────────▼───────────────────────────────────────┐
│                      Core Layer (Business Logic)                 │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    Services                                │  │
│  │              src/core/services/                            │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │          CivitaiService                              │  │  │
│  │  │  ┌────────────────────────────────────────────────┐  │  │  │
│  │  │  │  + generate_image()                            │  │  │  │
│  │  │  │  + get_job_status()                            │  │  │  │
│  │  │  │  + wait_for_completion()                       │  │  │  │
│  │  │  │  + download_image()                            │  │  │  │
│  │  │  └────────────────────────────────────────────────┘  │  │  │
│  │  └──────────────────────────────────────────────────────┘  │  │
│  └────────────────────────┬───────────────────────────────────┘  │
│                           │                                       │
│  ┌────────────────────────▼───────────────────────────────────┐  │
│  │                    Domain Models                           │  │
│  │              src/core/models/                              │  │
│  │  ┌──────────┐  ┌──────────┐  ┌────────────────────────┐   │  │
│  │  │ Image    │  │ Job      │  │ GenerationParams       │   │  │
│  │  └──────────┘  └──────────┘  └────────────────────────┘   │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    Configuration                           │  │
│  │              src/core/config/                              │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │  Settings (from .env + configs/*.yaml)               │  │  │
│  │  └──────────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                                │ Makes API calls
                                │
┌───────────────────────────────▼───────────────────────────────────┐
│                    External Services                              │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                  Civitai API                               │  │
│  │        (orchestration.civitai.com)                         │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │  │
│  │  │ Image Gen    │  │ Job Status   │  │ Blob Storage │     │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘     │  │
│  └────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
```

## Layer Communication Flow

### API Request Flow
```
HTTP Request
    │
    ▼
┌─────────────────┐
│  API Route      │  (src/api/routes/images.py)
│  images.py      │  - Validates HTTP request
└────────┬────────┘  - Extracts parameters
         │
         ▼
┌─────────────────┐
│ API Request DTO │  (src/contracts/api/requests.py)
│ GenerateImage   │  - Type validation
│ Request         │  - Business rules
└────────┬────────┘
         │
         │ Maps to
         ▼
┌─────────────────┐
│ Domain Model    │  (src/core/models/generation_params.py)
│ Generation      │  - Domain representation
│ Params          │  - Core business model
└────────┬────────┘
         │
         │ Passed to
         ▼
┌─────────────────┐
│ Service Method  │  (src/core/services/civitai_service.py)
│ generate_image()│  - Business logic
└────────┬────────┘  - API integration
         │
         ▼
┌─────────────────┐
│ Civitai API     │  (External)
│ POST /jobs      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Service Result  │  (src/core/models/job.py)
│ Job Model       │  - Domain result
└────────┬────────┘
         │
         │ Maps to
         ▼
┌─────────────────┐
│ API Response DTO│  (src/contracts/api/responses.py)
│ GenerateImage   │  - API-specific format
│ Response        │
└────────┬────────┘
         │
         ▼
     HTTP Response
```

### MCP Tool Flow
```
MCP Tool Call
    │
    ▼
┌─────────────────┐
│  MCP Tool       │  (src/mcp/tools/generate_image.py)
│  generate_image │  - Validates tool args
└────────┬────────┘  - Extracts parameters
         │
         ▼
┌─────────────────┐
│ Domain Model    │  (src/core/models/generation_params.py)
│ Generation      │  - Same core model as API
│ Params          │
└────────┬────────┘
         │
         │ Passed to
         ▼
┌─────────────────┐
│ Service Method  │  (src/core/services/civitai_service.py)
│ generate_image()│  - Same service as API uses
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Service Result  │  (src/core/models/job.py)
│ Job Model       │  - Same domain model
└────────┬────────┘
         │
         │ Formats as
         ▼
┌─────────────────┐
│ MCP Response    │  (src/contracts/mcp/responses.py)
│ ToolResponse    │  - MCP-specific format
└────────┬────────┘  - TextContent wrapper
         │
         ▼
    MCP Response
```

## File Organization

### API Layer Structure
```
src/api/
├── main.py                    # FastAPI app creation
│   └── Creates app
│       └── Includes routers
│
├── dependencies.py            # Dependency injection
│   └── get_civitai_service()
│
└── routes/
    ├── health.py             # Health endpoints
    │   ├── GET /
    │   └── GET /health
    │
    ├── images.py             # Image endpoints
    │   └── POST /images/generate
    │
    └── jobs.py               # Job endpoints
        └── GET /jobs/{token}
```

### MCP Layer Structure
```
src/mcp/
├── main.py                    # Entry point
│   └── Runs server
│
├── server.py                  # Server setup
│   ├── Creates MCP server
│   ├── Registers tools
│   └── Handles stdio
│
└── tools/
    ├── base.py               # Base tool class
    │   └── BaseTool
    │
    ├── generate_image.py     # Generate tool
    │   └── GenerateImageTool
    │       ├── definition()
    │       └── execute()
    │
    ├── check_job_status.py   # Status tool
    │   └── CheckJobStatusTool
    │       ├── definition()
    │       └── execute()
    │
    └── generate_and_wait.py  # Combined tool
        └── GenerateAndWaitTool
            ├── definition()
            └── execute()
```

### Core Layer Structure
```
src/core/
├── services/
│   ├── base.py
│   │   └── BaseService
│   │
│   └── civitai_service.py
│       └── CivitaiService
│           ├── __init__()
│           ├── generate_image()
│           ├── get_job_status()
│           ├── wait_for_completion()
│           └── download_image()
│
├── models/
│   ├── image.py
│   │   └── Image
│   │
│   ├── job.py
│   │   └── Job
│   │
│   └── generation_params.py
│       └── GenerationParams
│
└── config/
    └── settings.py
        └── Settings
```

## Dependency Graph

```
┌──────────────┐
│   API Layer  │──┐
└──────────────┘  │
                  │
┌──────────────┐  │
│   MCP Layer  │──┤
└──────────────┘  │
                  │
                  ├──> ┌──────────────────┐
                  │    │ Contracts Layer  │
                  │    └──────────────────┘
                  │              │
                  │              ▼
                  └──> ┌──────────────────┐
                       │   Core Layer     │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ External Services│
                       └──────────────────┘
```

## Data Flow Example: Generate Image

```
1. Client Request
   │
   ▼
2. API Route / MCP Tool
   │ Validates request
   │ Creates request DTO/extracts args
   ▼
3. Contract Layer
   │ Validates business rules
   │ Maps to domain model
   ▼
4. Core Service
   │ Executes business logic
   │ Calls Civitai API
   ▼
5. External API
   │ Returns job data
   ▼
6. Core Service
   │ Creates domain model (Job)
   ▼
7. Contract Layer
   │ Maps to response DTO
   ▼
8. API Route / MCP Tool
   │ Formats response
   ▼
9. Client Response
```

## Separation of Concerns

### ✅ API Layer
- **Knows about:** HTTP, FastAPI, request/response
- **Doesn't know about:** MCP, Civitai API details
- **Responsibility:** HTTP interface

### ✅ MCP Layer
- **Knows about:** MCP protocol, stdio, tools
- **Doesn't know about:** HTTP, FastAPI
- **Responsibility:** MCP interface

### ✅ Contracts Layer
- **Knows about:** Data validation, DTO structure
- **Doesn't know about:** Business logic, external APIs
- **Responsibility:** Interface definitions

### ✅ Core Layer
- **Knows about:** Business logic, domain models
- **Doesn't know about:** HTTP, MCP, protocols
- **Responsibility:** Business logic

## Benefits Visualization

```
Before (Monolithic)
┌─────────────────────────────────────┐
│  Everything in one file/module      │
│  • Routes + Logic + API calls       │
│  • Hard to test                     │
│  • Hard to maintain                 │
│  • Tight coupling                   │
└─────────────────────────────────────┘

After (Layered)
┌────────────┐  ┌────────────┐
│ API Layer  │  │ MCP Layer  │  Small, focused
└─────┬──────┘  └──────┬─────┘  Easy to modify
      │                │
      └────────┬───────┘
               │
      ┌────────▼─────────┐
      │ Contracts Layer  │        Clear boundaries
      └────────┬─────────┘        Type-safe
               │
      ┌────────▼─────────┐
      │   Core Layer     │        Testable
      └────────┬─────────┘        Reusable
               │
      ┌────────▼─────────┐
      │ External Services│        Isolated
      └──────────────────┘
```

This architecture ensures:
- ✅ Clear separation of concerns
- ✅ Easy to test each layer
- ✅ Easy to add new interfaces
- ✅ Core logic is reusable
- ✅ Changes are isolated
