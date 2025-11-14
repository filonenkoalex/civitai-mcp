# CivitAI MCP Server - Quick Start Guide

## 📋 Project Overview

**CivitAI MCP** is a Model Context Protocol server that enables AI agents to generate images using CivitAI's platform.

### Key Features
- 🤖 **4 MCP Tools**: generate_image, enhance_prompt, list_models, get_generation_status
- 🎨 **Smart Prompt Enhancement**: AI-powered prompt optimization
- 🎯 **Model Intelligence**: Automatic model suggestions
- 🔌 **MCP Compatible**: Works with LM Studio, Claude Desktop, and more
- 🚀 **Developer Friendly**: Bun + TypeScript with great DX

---

## 📚 Documentation Structure

```
docs/
├── 📖 requirements.md          # What to build (features & specs)
├── 🗓️ implementation.plan.md   # How to build it (8 phases)
├── 🏗️ project.structure.md     # Architecture & code organization
├── 🛣️ development.roadmap.md   # Timeline & milestones (8 days)
├── 🎯 planning.overview.md     # Master planning guide
└── ⚡ quickstart.md            # This file (get started fast)
```

**Start here**, then dive deeper based on your needs:
- **Building?** → Read `implementation.plan.md`
- **Architecture?** → Read `project.structure.md`
- **Timeline?** → Read `development.roadmap.md`

---

## 🎯 Requirements at a Glance

### Core Functionality
1. **Image Generation** - Generate images from text prompts
2. **Prompt Enhancement** - AI-powered prompt optimization
3. **Model Management** - List and select models
4. **Status Tracking** - Monitor generation progress

### Technical Stack
- **Runtime**: Bun
- **Language**: TypeScript (strict mode)
- **MCP SDK**: @modelcontextprotocol/sdk
- **CivitAI**: civitai npm package

### Quality Standards
- ✅ 80% test coverage
- ✅ Zero TypeScript errors
- ✅ Zero linting errors
- ✅ Comprehensive documentation
- ✅ Production-ready code

---

## 🗓️ Implementation Phases

| Phase | Duration | Focus | Key Deliverable |
|-------|----------|-------|-----------------|
| **Phase 1** | Day 1 | Foundation | Working MCP server skeleton |
| **Phase 2** | Day 2 | CivitAI Integration | API connection & services |
| **Phase 3** | Day 3 | MCP Tools | All 4 tools functional |
| **Phase 4** | Day 4 | Prompt Intelligence | Smart enhancement & suggestions |
| **Phase 5** | Day 5 | Developer Experience | Build system & scripts |
| **Phase 6** | Day 6 | Testing & QA | 80% coverage, all tests pass |
| **Phase 7** | Day 7 | Documentation | Complete docs & examples |
| **Phase 8** | Day 8 | Integration & Polish | LM Studio & Claude working |

**Total: 8 days** for production-ready MCP server

---

## 🏗️ Project Structure

```
src/
├── index.ts              # Entry point
├── server/               # MCP server layer
│   ├── CivitaiMCPServer.ts
│   └── config.ts
├── tools/                # MCP tools (4 tools)
│   ├── generateImage.ts
│   ├── enhancePrompt.ts
│   ├── listModels.ts
│   └── getGenerationStatus.ts
├── services/             # Business logic
│   ├── CivitaiService.ts    # API wrapper
│   ├── PromptService.ts     # Prompt enhancement
│   ├── ModelService.ts      # Model management
│   └── JobService.ts        # Job tracking
├── types/                # TypeScript types
├── utils/                # Utilities
└── constants/            # Config & constants
```

---

## 🚀 Getting Started (For Developers)

### Prerequisites
- [Bun](https://bun.sh) installed
- Node.js 18+ (for compatibility)
- CivitAI API token

### Setup Steps

1. **Clone and Install**
   ```bash
   git clone <repository>
   cd civitai-mcp
   bun install
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your CIVITAI_API_TOKEN
   ```

3. **Start Development**
   ```bash
   bun run dev          # Start with watch mode
   ```

4. **Build for Production**
   ```bash
   bun run build        # Compile TypeScript
   bun run start        # Run compiled code
   ```

### Available Scripts

```bash
bun run dev          # Development with watch mode
bun run build        # Production build
bun run start        # Run production build
bun run test         # Run test suite
bun run test:watch   # Run tests in watch mode
bun run lint         # Run ESLint
bun run typecheck    # Run TypeScript type check
bun run clean        # Clean build artifacts
```

---

## 🧪 Testing Strategy

### Test Structure
```
tests/
├── unit/           # Unit tests
│   ├── services/   # Service layer tests
│   ├── tools/      # Tool tests
│   └── utils/      # Utility tests
├── integration/    # Integration tests
└── mocks/          # Test mocks
```

### Running Tests
```bash
bun run test              # All tests
bun run test:watch        # Watch mode
bun test tests/unit/      # Specific directory
bun test specific.test.ts # Specific file
```

### Coverage Goal: 80%
```bash
bun run test --coverage   # Check coverage
```

---

## 🔧 Development Workflow

### Daily Development
1. **Start Day**: Review current phase in `implementation.plan.md`
2. **During Day**:
   - Implement assigned tasks
   - Write tests for new code
   - Run `bun run lint` and `bun run typecheck`
   - Commit frequently
3. **End Day**: Verify acceptance criteria

### Code Quality Checks (Run Before Commit)
```bash
bun run lint       # Should show no errors
bun run typecheck  # Should pass
bun run test       # All tests should pass
```

---

## 📦 MCP Tools Reference

### 1. generate_image
Generate images from text prompts.

**Input:**
```typescript
{
  prompt: string,              // Image description
  model?: string,              // Model URN (optional)
  params?: {                   // Generation parameters
    width?: number,
    height?: number,
    steps?: number,
    cfgScale?: number
  }
}
```

**Output:**
```typescript
{
  imageUrl: string,            // Generated image URL
  metadata: object             // Generation metadata
}
```

### 2. enhance_prompt
Enhance user prompts for better results.

**Input:**
```typescript
{
  userDescription: string,     // User's basic description
  style?: string               // Desired style (optional)
}
```

**Output:**
```typescript
{
  enhancedPrompt: string,      // Optimized prompt
  modelSuggestions: string[]   // Recommended models
}
```

### 3. list_models
List available CivitAI models.

**Input:**
```typescript
{
  category?: string,           // Model category (optional)
  limit?: number               // Max results (optional)
}
```

**Output:**
```typescript
{
  models: Array<{              // Available models
    id: string,
    name: string,
    description: string
  }>
}
```

### 4. get_generation_status
Check image generation status.

**Input:**
```typescript
{
  jobToken: string             // Job token from generate_image
}
```

**Output:**
```typescript
{
  status: string,              // 'pending', 'processing', 'completed', 'failed'
  progress: number,            // 0-100
  resultUrl?: string           // Image URL if completed
}
```

---

## 🔐 Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Required
CIVITAI_API_TOKEN=your_api_token_here

# Optional (with defaults)
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=3000
LOG_LEVEL=info
DEFAULT_MODEL=urn:air:sd1:checkpoint:civitai:4201@130072
```

**Get your CivitAI API token**: https://civitai.com/user/account

---

## 🤝 Integration with AI Agents

### LM Studio Setup
1. Install LM Studio
2. Add MCP server configuration:
   ```json
   {
     "mcpServers": {
       "civitai": {
         "command": "npx",
         "args": ["civitai-mcp"],
         "env": {
           "CIVITAI_API_TOKEN": "your_token"
         }
       }
     }
   }
   ```

### Claude Desktop Setup
1. Install Claude Desktop
2. Add to MCP configuration:
   ```json
   {
     "mcpServers": {
       "civitai": {
         "command": "npx",
         "args": ["civitai-mcp"],
         "env": {
           "CIVITAI_API_TOKEN": "your_token"
         }
       }
     }
   }
   ```

### Usage Example
```
User: "Generate an image of a sunset over mountains"
AI: "I'll generate that image for you."
[AI uses generate_image tool]
AI: "Here's your generated image: [URL]"
```

---

## ✅ Requirements Satisfaction Checklist

### Functionality
- [ ] MCP server starts and accepts connections
- [ ] 4 MCP tools implemented and working
- [ ] CivitAI API integration functional
- [ ] Image generation produces results
- [ ] Prompt enhancement improves quality
- [ ] Model listing and selection works
- [ ] Job status tracking works

### Code Quality
- [ ] TypeScript strict mode enabled
- [ ] 80% test coverage achieved
- [ ] Zero linting errors
- [ ] Zero type errors
- [ ] Clean, maintainable code
- [ ] Proper error handling

### Documentation
- [ ] README with setup instructions
- [ ] API documentation complete
- [ ] Setup guides for LM Studio & Claude
- [ ] Working examples provided
- [ ] Code comments and JSDoc

### Integration
- [ ] Works with LM Studio
- [ ] Works with Claude Desktop
- [ ] Natural language prompts work
- [ ] Error messages are helpful

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Cannot connect to CivitAI API"
- **Solution**: Check CIVITAI_API_TOKEN in .env file
- **Verify**: Run `bun run test` to check API connection

**Issue**: "MCP tools not showing up"
- **Solution**: Restart the MCP server
- **Verify**: Check server logs for tool registration

**Issue**: "TypeScript errors"
- **Solution**: Run `bun run typecheck` to see errors
- **Fix**: Address all type errors before running

**Issue**: "Tests failing"
- **Solution**: Run `bun run test` to see failures
- **Check**: Ensure .env file is configured

### Getting Help

1. Check `docs/` folder for detailed documentation
2. Review examples in `docs/examples/`
3. Check troubleshooting section in README
4. Verify all requirements in `docs/requirements.md`

---

## 🎯 Next Steps

### For New Developers
1. ✅ Read this quickstart guide
2. 📖 Read `docs/requirements.md` for full specifications
3. 🗓️ Review `docs/implementation.plan.md` for development phases
4. 🏗️ Study `docs/project.structure.md` for architecture
5. 🚀 Start with Phase 1 tasks

### For Project Review
1. 📋 Review `docs/requirements.md` - confirm requirements
2. 🗓️ Review `docs/development.roadmap.md` - confirm timeline
3. ✅ Verify acceptance criteria for each milestone
4. 🎯 Ensure requirements traceability

---

## 📊 Progress Tracking

### Current Phase
Refer to `docs/implementation.plan.md` for current phase details

### Milestone Status
Refer to `docs/development.roadmap.md` for milestone progress

### Requirements Coverage
Refer to `docs/planning.overview.md` for traceability matrix

---

## 🎉 Success Criteria

Project is successful when:
- ✅ All 4 MCP tools work correctly
- ✅ Can generate images via natural language
- ✅ Prompt enhancement improves quality
- ✅ Works with LM Studio and Claude Desktop
- ✅ 80% test coverage achieved
- ✅ Zero TypeScript and linting errors
- ✅ Complete documentation provided
- ✅ Production-ready code

**Estimated Timeline**: 8 days

---

*For detailed information, refer to the specific documentation files in the `docs/` folder.*
