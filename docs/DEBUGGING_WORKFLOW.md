# MCP Debugging Workflow

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Your Development Setup                  │
└─────────────────────────────────────────────────────────────┘

┌────────────────────────┐         ┌──────────────────────────┐
│   VS Code (Terminal 1) │         │  Browser (MCP Inspector) │
│                        │         │                          │
│  ┌──────────────────┐  │         │  ┌────────────────────┐  │
│  │  Python Debugger │  │         │  │  Tool Interface    │  │
│  │    (debugpy)     │  │         │  │                    │  │
│  │                  │  │         │  │  • generate_image  │  │
│  │  • Breakpoints   │  │         │  │                    │  │
│  │  • Variables     │  │         │  │  [Execute Tool]    │  │
│  │  • Call Stack    │  │         │  └────────┬───────────┘  │
│  │  • Step Through  │  │         │           │              │
│  └────────┬─────────┘  │         └───────────┼──────────────┘
│           │            │                     │
│           │ debugging  │                     │
│           ▼            │                     │
│  ┌──────────────────┐  │                     │ JSON-RPC
│  │  MCP Server      │  │◄────────────────────┘ over stdio
│  │                  │  │
│  │  src/mcp/server  │  │
│  │  • generate_image│  │
│  └────────┬─────────┘  │
│           │            │
│           │ calls      │
│           ▼            │
│  ┌──────────────────┐  │
│  │  Civitai Service │  │
│  │                  │  │
│  │  • API calls     │  │
│  │  • Job polling   │  │
│  └────────┬─────────┘  │
└───────────┼────────────┘
            │
            │ HTTPS
            ▼
   ┌─────────────────┐
   │   Civitai API   │
   │ (External)      │
   └─────────────────┘
```

## Step-by-Step Flow

### 1. Setup Phase
```
Developer              VS Code                 MCP Inspector
    │                     │                          │
    │   Set breakpoints   │                          │
    ├────────────────────>│                          │
    │                     │                          │
    │   Press F5          │                          │
    ├────────────────────>│                          │
    │                     │ Start debug server       │
    │                     │ (stdio interface ready)  │
    │                     │                          │
```

### 2. Connection Phase
```
Developer              VS Code                 MCP Inspector
    │                     │                          │
    │   Run debug script  │                          │
    ├─────────────────────┼─────────────────────────>│
    │                     │                          │
    │                     │ ◄────Connect stdio──────┤
    │                     │                          │
    │                     │ ◄────List tools─────────┤
    │                     │ ─────Tools info────────>│
    │                     │                          │
    │                     │      Inspector UI opens  │
```

### 3. Debugging Phase
```
Developer              VS Code                 MCP Inspector
    │                     │                          │
    │                     │                     ┌────┴────┐
    │                     │                     │ User    │
    │                     │                     │ clicks  │
    │                     │                     │ Execute │
    │                     │                     └────┬────┘
    │                     │                          │
    │                     │ ◄──Tool call (JSON)─────┤
    │                     │                          │
    │                 ⚡ BREAKPOINT HIT! ⚡           │
    │                     │                          │
    │◄──Variables inspect─┤                          │
    │   Call stack        │                          │
    │                     │                          │
    │   Press F10 (step)  │                          │
    ├────────────────────>│                          │
    │                     │ Execute next line        │
    │                     │                          │
    │   Press F5 (continue)                          │
    ├────────────────────>│                          │
    │                     │ Continue execution       │
    │                     │ ─────API call───────────>│
    │                     │                     (Civitai)
    │                     │ ◄────Response────────────┤
    │                     │                          │
    │                     │ ─────Result (base64)────>│
    │                     │                          │
    │                     │                     ┌────┴────┐
    │                     │                     │ Display │
    │                     │                     │ image   │
    │                     │                     └─────────┘
```

## File Structure for Debugging

```
civitai-mcp/
├── .vscode/
│   ├── launch.json          # ← Debug configurations
│   └── settings.json        # ← Python settings
│
├── scripts/
│   └── debug_with_inspector.sh  # ← Quick debug script
│
├── docs/
│   └── DEBUGGING.md         # ← Detailed guide
│
└── src/
    └── mcp/
        └── server.py        # ← Your breakpoints go here!
```

## Common Debugging Scenarios

### Scenario 1: Debug Parameter Validation
```python
# src/mcp/server.py:45
@mcp.tool()
async def generate_image(...):
    # Set breakpoint here ⬇️
    request = GenerateImageRequest(
        model=model,
        prompt=prompt,
        ...
    )
    # Inspect: request.__dict__
```

### Scenario 2: Debug API Communication
```python
# src/core/services/civitai_service.py
async def generate_and_download(self, ...):
    # Set breakpoint here ⬇️
    response = await self._submit_job(request)
    # Inspect: response.status, response.headers
    
    # Set breakpoint here ⬇️
    result = await self._poll_job(token, ...)
    # Inspect: result['status'], result['jobs']
```

### Scenario 3: Debug Response Encoding
```python
# src/mcp/server.py:64
@mcp.tool()
async def generate_image(...):
    result = await service.generate_and_download(...)
    
    # Set breakpoint here ⬇️
    image_b64 = base64.b64encode(result['image_data'])
    # Inspect: len(result['image_data']), image_b64[:100]
    
    return f"data:image/png;base64,{image_b64}"
```

## Quick Reference

### VS Code Shortcuts
- `F5` - Start/Continue debugging
- `F9` - Toggle breakpoint
- `F10` - Step over
- `F11` - Step into
- `Shift+F11` - Step out
- `Ctrl+Shift+F5` - Restart debugging
- `Shift+F5` - Stop debugging

### Debug Console Commands
```python
# Print variables
print(request)
print(request.__dict__)

# Evaluate expressions
len(prompt)
f"{width}x{height}"

# Import and use libraries
import json
json.dumps(result, indent=2)
```

### Inspector Actions
- **Connect** - Establishes stdio connection to MCP server
- **List Tools** - Shows available tools (auto-called on connect)
- **Execute Tool** - Calls your tool function
- **View Request/Response** - Shows JSON-RPC messages

## Environment Setup Checklist

- [ ] Python virtual environment activated (`.venv`)
- [ ] Dependencies installed (`uv sync`)
- [ ] `.env` file with `CIVITAI_API_TOKEN` exists
- [ ] MCP Inspector installed (`npm install -g @modelcontextprotocol/inspector`)
- [ ] VS Code Python extension installed
- [ ] Workspace opened in VS Code

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Breakpoints not hit | Set `"justMyCode": false` in launch.json ✅ |
| Inspector won't connect | Start debug server in VS Code first |
| Import errors | Run `uv sync` and restart VS Code |
| Token errors | Check `.env` file exists and is loaded |
| Port conflicts | MCP uses stdio, not ports - check terminal output |

## Pro Tips

💡 **Use Conditional Breakpoints** - Only break on specific conditions
```python
# Right-click breakpoint → Edit Breakpoint → Condition:
prompt.startswith("test")
```

💡 **Use Logpoints** - Log without stopping
```python
# Right-click → Add Logpoint:
Request for model: {model}, size: {width}x{height}
```

💡 **Watch Expressions** - Auto-evaluate on each step
```python
# Add to Watch pane:
request.model
len(image_data)
```

💡 **Exception Breakpoints** - Break on any exception
```
# Debug sidebar → Breakpoints → Check "Raised Exceptions"
```

## Next Steps

1. ✅ Read [DEBUGGING.md](DEBUGGING.md) for detailed instructions
2. ✅ Try the example debugging scenarios above
3. ✅ Experiment with different breakpoint types
4. ✅ Learn the VS Code debugging shortcuts

Happy debugging! 🐛🔍

