# CivitAI MCP Server - Requirements

## Project Overview

CivitAI MCP is a Model Context Protocol server that enables AI agents (like LM Studio, Claude, etc.) to generate images using the CivitAI platform. The server provides tools for text-to-image generation, prompt enhancement, and model management, allowing seamless integration with AI assistants.

## User Experience Requirements

### Core Functionality
- **Image Generation**: Users can request image generation with natural language prompts
- **Prompt Enhancement**: AI can create optimized prompts for better image quality
- **Model Selection**: Automatic or manual selection of appropriate models
- **Image Delivery**: Generated images returned as direct URLs in JPEG/PNG format
- **Progress Tracking**: Real-time status updates during generation

### Integration Experience
- **MCP Compatibility**: Works with any MCP-compatible AI agent (LM Studio, Claude Desktop, etc.)
- **Natural Language**: Users describe what they want in plain English
- **Seamless Workflow**: AI can generate prompts, select models, and create images in one conversation
- **Error Handling**: Clear error messages and recovery suggestions

## Technical Requirements

### Technology Stack
- **Runtime**: Bun (fast JavaScript runtime)
- **Language**: TypeScript with strict mode
- **MCP SDK**: @modelcontextprotocol/sdk
- **CivitAI SDK**: civitai npm package
- **Package Manager**: Bun (native support)

### MCP Server Specifications

#### Tools
1. **generate_image**
   - Input: prompt (string), model (optional string), parameters (optional object)
   - Output: image URL, generation metadata
   - Description: Generate image from text prompt

2. **enhance_prompt**
   - Input: user_description (string), style (optional string)
   - Output: enhanced_prompt (string), model_suggestions (array)
   - Description: Optimize user description into detailed prompt

3. **list_models**
   - Input: category (optional string), limit (optional number)
   - Output: available_models (array of model objects)
   - Description: Get list of available CivitAI models

4. **get_generation_status**
   - Input: job_token (string)
   - Output: status (string), progress (number), result_url (optional string)
   - Description: Check status of image generation job

#### Resources (Optional)
- **Model Information**: Static resources about available models
- **Prompt Templates**: Pre-defined prompt templates for common use cases
- **Style Guides**: Reference materials for different art styles

### Architecture & Folder Structure

```
civitai-mcp/
├── src/
│   ├── index.ts                 # Main entry point
│   ├── server/                  # MCP server implementation
│   │   ├── CivitaiMCPServer.ts  # Main server class
│   │   └── config.ts            # Server configuration
│   ├── tools/                   # MCP tools implementation
│   │   ├── generateImage.ts     # Image generation tool
│   │   ├── enhancePrompt.ts     # Prompt enhancement tool
│   │   ├── listModels.ts        # Model listing tool
│   │   └── getGenerationStatus.ts # Status checking tool
│   ├── services/                # Business logic layer
│   │   ├── CivitaiService.ts    # CivitAI API wrapper
│   │   ├── PromptService.ts     # Prompt processing logic
│   │   └── ModelService.ts      # Model management logic
│   ├── types/                   # TypeScript type definitions
│   │   ├── mcp.ts               # MCP-related types
│   │   ├── civitai.ts           # CivitAI API types
│   │   └── index.ts             # Type exports
│   ├── utils/                   # Utility functions
│   │   ├── logger.ts            # Logging utility
│   │   ├── validators.ts        # Input validation
│   │   └── errors.ts            # Error handling
│   └── constants/               # Constants and configuration
│       ├── models.ts            # Default model configurations
│       └── prompts.ts           # Prompt templates
├── tests/                       # Test files
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
├── scripts/                     # Build and development scripts
│   ├── build.ts                 # Build script
│   └── dev.ts                   # Development script
├── docs/                        # Documentation
│   ├── setup.md                 # Setup instructions
│   └── api.md                   # API documentation
├── dist/                        # Compiled output
├── .env.example                 # Environment variables template
├── package.json                 # Dependencies and scripts
├── tsconfig.json               # TypeScript configuration
├── bun.lockb                   # Bun lock file
└── requirements.md             # This file
```

### Development Experience Requirements

#### Build System
- **Fast Compilation**: Bun's native TypeScript support
- **Watch Mode**: Automatic recompilation on file changes
- **Source Maps**: Debuggable source code
- **Clean Output**: Organized dist folder with proper structure

#### Scripts
```json
{
  "scripts": {
    "dev": "bun run --watch src/index.ts",
    "build": "bun build src/index.ts --outdir=dist --target=node",
    "start": "bun run dist/index.js",
    "test": "bun test",
    "test:watch": "bun test --watch",
    "lint": "bun x eslint src/**/*.ts",
    "typecheck": "bun x tsc --noEmit",
    "clean": "rm -rf dist",
    "prepare": "bun run build"
  }
}
```

#### Environment Configuration
- **API Token**: CIVITAI_API_TOKEN (required)
- **Server Settings**: MCP server host/port configuration
- **Logging**: Log level configuration
- **Defaults**: Default model, image dimensions, etc.

### Code Quality Requirements

#### TypeScript Configuration
- **Strict Mode**: Enabled for type safety
- **No Implicit Any**: All types must be explicit
- **ES2022**: Modern JavaScript features
- **Declaration Files**: Generate .d.ts for library usage

#### Code Patterns
- **Dependency Injection**: Services injected for testability
- **Error Boundaries**: Comprehensive error handling
- **Async/Await**: Modern async patterns
- **Interface Segregation**: Small, focused interfaces
- **Single Responsibility**: Each module has one purpose

#### Testing Strategy
- **Unit Tests**: Individual function testing
- **Integration Tests**: MCP protocol testing
- **Mock Services**: CivitAI API mocking for tests
- **Coverage**: Minimum 80% code coverage

### Security Requirements
- **API Token Protection**: Never log or expose API tokens
- **Input Validation**: Sanitize all user inputs
- **Rate Limiting**: Respect CivitAI API limits
- **Error Messages**: Don't leak sensitive information

### Performance Requirements
- **Connection Pooling**: Reuse CivitAI client connections
- **Caching**: Cache model lists and prompt templates
- **Timeout Handling**: Proper timeout for long-running operations
- **Memory Management**: Clean up resources properly

### Documentation Requirements
- **README**: Setup and usage instructions
- **API Docs**: Detailed tool descriptions
- **Examples**: Sample prompts and expected outputs
- **Troubleshooting**: Common issues and solutions

## Success Criteria

1. **Functionality**: All MCP tools work correctly with CivitAI API
2. **Integration**: Successfully connects to LM Studio and other MCP clients
3. **User Experience**: Natural language image generation works seamlessly
4. **Code Quality**: Passes linting, type checking, and tests
5. **Documentation**: Complete setup and usage documentation
6. **Performance**: Image generation completes within acceptable timeframes

## Future Enhancements

- **Image-to-Image**: Support for img2img generation
- **Batch Processing**: Generate multiple images at once
- **Model Fine-tuning**: Support for custom model uploads
- **Prompt History**: Track and reuse previous prompts
- **Gallery Integration**: Browse and manage generated images
- **Advanced Parameters**: Support for all CivitAI generation parameters
