# CivitAI MCP Server - Project Structure

## High-Level Architecture

```
civitai-mcp/
├── src/                          # Source code
│   ├── index.ts                  # Application entry point
│   │
│   ├── server/                   # MCP Server Layer
│   │   ├── CivitaiMCPServer.ts   # Main server orchestrator
│   │   ├── config.ts             # Server configuration
│   │   └── types.ts              # Server-specific types
│   │
│   ├── tools/                    # MCP Tools Layer
│   │   ├── generateImage.ts      # Image generation tool
│   │   ├── enhancePrompt.ts      # Prompt enhancement tool
│   │   ├── listModels.ts         # Model listing tool
│   │   ├── getGenerationStatus.ts # Status checking tool
│   │   └── index.ts              # Tool exports and registration
│   │
│   ├── services/                 # Business Logic Layer
│   │   ├── CivitaiService.ts     # CivitAI API wrapper
│   │   ├── PromptService.ts      # Prompt processing & enhancement
│   │   ├── ModelService.ts       # Model management & selection
│   │   └── JobService.ts         # Job tracking & status management
│   │
│   ├── types/                    # Type Definitions
│   │   ├── mcp.ts                # MCP protocol types
│   │   ├── civitai.ts            # CivitAI API types
│   │   ├── internal.ts           # Internal application types
│   │   └── index.ts              # Type exports
│   │
│   ├── utils/                    # Utility Functions
│   │   ├── logger.ts             # Logging utility
│   │   ├── validators.ts         # Input validation
│   │   ├── errors.ts             # Error handling & custom errors
│   │   ├── cache.ts              # Caching utilities
│   │   └── helpers.ts            # Common helper functions
│   │
│   └── constants/                # Constants & Configuration
│       ├── models.ts             # Default model configurations
│       ├── prompts.ts            # Prompt templates & examples
│       └── config.ts             # Application constants
│
├── tests/                        # Test Suite
│   ├── unit/                     # Unit tests
│   │   ├── services/             # Service layer tests
│   │   ├── tools/                # Tool layer tests
│   │   └── utils/                # Utility tests
│   ├── integration/              # Integration tests
│   │   ├── mcp-protocol.test.ts  # MCP protocol tests
│   │   └── end-to-end.test.ts    # End-to-end workflow tests
│   └── mocks/                    # Test mocks & fixtures
│       ├── civitai.mock.ts       # CivitAI API mocks
│       └── data/                 # Mock data files
│
├── scripts/                      # Build & Development Scripts
│   ├── build.ts                  # Production build script
│   ├── dev.ts                    # Development script with watch
│   └── test.ts                   # Test runner script
│
├── docs/                         # Documentation
│   ├── requirements.md           # Project requirements
│   ├── implementation.plan.md    # Implementation plan
│   ├── project.structure.md      # This file
│   ├── setup.md                  # Setup instructions
│   ├── api.md                    # API documentation
│   └── examples/                 # Usage examples
│       ├── basic-generation.md   # Basic image generation
│       ├── prompt-enhancement.md # Prompt enhancement examples
│       └── model-selection.md    # Model selection examples
│
├── dist/                         # Compiled output (generated)
├── node_modules/                 # Dependencies (generated)
│
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── .eslintrc.json                # ESLint configuration
├── package.json                  # Dependencies & scripts
├── tsconfig.json                 # TypeScript configuration
├── bun.lockb                     # Bun lock file
└── README.md                     # Project README
```

## Component Responsibilities

### 1. Server Layer (`src/server/`)
**Purpose**: MCP protocol implementation and server lifecycle management

**CivitaiMCPServer.ts**:
- Initialize MCP server using @modelcontextprotocol/sdk
- Register all available tools
- Handle client connections
- Manage server lifecycle (start/stop)
- Error handling at server level

**config.ts**:
- Server configuration (host, port)
- MCP protocol version
- Connection settings

### 2. Tools Layer (`src/tools/`)
**Purpose**: MCP tool definitions and request handling

**generateImage.ts**:
- Tool definition for `generate_image`
- Input: prompt, model, parameters
- Process: Validate → Call CivitaiService → Return result
- Output: image URL, metadata

**enhancePrompt.ts**:
- Tool definition for `enhance_prompt`
- Input: user description, style
- Process: Analyze → Call PromptService → Return enhanced prompt
- Output: enhanced prompt, model suggestions

**listModels.ts**:
- Tool definition for `list_models`
- Input: category, limit
- Process: Call ModelService → Return filtered models
- Output: array of model objects

**getGenerationStatus.ts**:
- Tool definition for `get_generation_status`
- Input: job_token
- Process: Call JobService → Return status
- Output: status, progress, result_url

### 3. Services Layer (`src/services/`)
**Purpose**: Business logic and external API integration

**CivitaiService.ts**:
- Wrap civitai npm package
- Handle authentication
- API call abstraction
- Error handling and retries
- Response parsing

**PromptService.ts**:
- Prompt analysis and enhancement
- Template processing
- Style-based optimization
- Negative prompt generation
- Parameter recommendations

**ModelService.ts**:
- Model discovery and caching
- Model metadata management
- Model selection logic
- Category filtering

**JobService.ts**:
- Job status tracking
- Polling mechanism
- Result extraction
- Timeout handling

### 4. Types Layer (`src/types/`)
**Purpose**: TypeScript type definitions for type safety

**mcp.ts**:
- MCP protocol types
- Tool input/output types
- Server configuration types

**civitai.ts**:
- CivitAI API request/response types
- Model types
- Job status types

**internal.ts**:
- Internal application types
- Service interfaces
- Configuration types

### 5. Utilities Layer (`src/utils/`)
**Purpose**: Common utilities and cross-cutting concerns

**logger.ts**:
- Structured logging
- Log levels (error, warn, info, debug)
- Formatting and output

**validators.ts**:
- Input validation functions
- Schema validation
- Error messages

**errors.ts**:
- Custom error classes
- Error handling utilities
- Error translation

**cache.ts**:
- In-memory caching
- Cache invalidation
- Performance optimization

### 6. Constants Layer (`src/constants/`)
**Purpose**: Application constants and default configurations

**models.ts**:
- Default model configurations
- Model categories
- Recommended models

**prompts.ts**:
- Prompt templates
- Style examples
- Best practices

**config.ts**:
- Application constants
- Default values
- Configuration options

## Data Flow

### Image Generation Flow
```
User Request (via MCP)
    ↓
tools/generateImage.ts
    ↓
services/CivitaiService.ts
    ↓
CivitAI API
    ↓
services/JobService.ts (for status)
    ↓
Return Image URL
```

### Prompt Enhancement Flow
```
User Description (via MCP)
    ↓
tools/enhancePrompt.ts
    ↓
services/PromptService.ts
    ↓
ModelService (for suggestions)
    ↓
Return Enhanced Prompt + Models
```

### Model Listing Flow
```
User Request (via MCP)
    ↓
tools/listModels.ts
    ↓
services/ModelService.ts
    ↓
services/CivitaiService.ts (if not cached)
    ↓
Return Model List
```

## Key Design Patterns

### 1. Dependency Injection
- Services are injected into tools
- Easy to mock for testing
- Loose coupling

### 2. Repository Pattern
- Services abstract external APIs
- Easy to swap implementations
- Centralized business logic

### 3. Factory Pattern
- Tool creation and registration
- Model instance creation
- Configuration object creation

### 4. Strategy Pattern
- Different prompt enhancement strategies
- Model selection strategies
- Error handling strategies

## Module Dependencies

```
index.ts
    ↓ (imports)
server/CivitaiMCPServer.ts
    ↓ (imports)
tools/index.ts (all tools)
    ↓ (imports)
services/ (CivitaiService, PromptService, ModelService, JobService)
    ↓ (imports)
utils/ (logger, validators, errors, cache)
types/ (all type definitions)
constants/ (models, prompts, config)
```

## Testing Strategy

### Unit Tests
- Test individual functions in isolation
- Mock external dependencies
- Fast execution

### Integration Tests
- Test tool workflows end-to-end
- Test MCP protocol compliance
- Mock CivitAI API

### End-to-End Tests
- Test with real MCP clients
- Test natural language workflows
- Verify image generation quality

## Scalability Considerations

### Horizontal Scaling
- Stateless design allows multiple instances
- External caching for model data
- Shared job tracking database (future)

### Performance Optimization
- Connection pooling for CivitAI API
- In-memory caching for models and prompts
- Async/await for non-blocking operations
- Efficient polling for job status

### Resource Management
- Proper cleanup of connections
- Timeout handling for long operations
- Memory usage monitoring

## Security Considerations

### API Token Protection
- Never log API tokens
- Secure storage in environment variables
- Token validation on startup

### Input Validation
- Sanitize all user inputs
- Validate prompt content
- Prevent prompt injection

### Rate Limiting
- Respect CivitAI API limits
- Implement client-side throttling
- Queue management for multiple requests

This structure ensures clean separation of concerns, maintainability, and scalability while following best practices for TypeScript and MCP server development.
