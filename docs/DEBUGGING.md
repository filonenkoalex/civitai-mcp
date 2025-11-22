# Debugging Guide

This guide explains how to debug your MCP server in VS Code while testing with MCP Inspector.

## Quick Start

### Option 1: Debug with Breakpoints (Recommended)

This is the best way to debug - you can set breakpoints and step through code as MCP Inspector triggers your tools.

1. **Set Breakpoints** in VS Code
   - Open `/home/ofilonenko/Projects/civitai-mcp/src/mcp/server.py`
   - Click left of line numbers to add breakpoints (e.g., line 45 in `generate_image`)

2. **Start Debug Session**
   - Press `F5` or go to Run > Start Debugging
   - Select "Debug MCP Server (Direct)"
   - The debug console will show the server starting

3. **Connect MCP Inspector**
   - Open a new terminal
   - Run: `./scripts/debug_with_inspector.sh`
   - Inspector will open in your browser (usually http://localhost:5173)

4. **Trigger Tools**
   - In the Inspector UI, you'll see your `generate_image` tool
   - Fill in the parameters and execute
   - VS Code will hit your breakpoints!

### Option 2: Simple Logging Debug

If you just want to see logs without breakpoints:

1. Add logging to your code:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In your tool function:
logger.debug(f"Received request: {request}")
```

2. Run normally and check the output

## VS Code Debug Configurations

### Configuration 1: Debug MCP Server (Direct)
- **Best for**: Quick debugging with breakpoints
- **Uses**: Python directly from your virtual environment
- **Stdio**: Connects properly with MCP Inspector

### Configuration 2: Debug MCP Server (with uv)
- **Best for**: Testing exactly as it runs in production
- **Uses**: uv to manage the environment
- **Stdio**: Connects properly with MCP Inspector

## Debugging Workflow

### Step-by-Step Example

Let's debug the `generate_image` tool:

1. **Add a breakpoint** at line 45 in `src/mcp/server.py` (where GenerateImageRequest is created)

2. **Start debugging** (F5) and select "Debug MCP Server (Direct)"

3. **Run the inspector** in another terminal:
```bash
./scripts/debug_with_inspector.sh
```

4. **In the Inspector**, test with:
```json
{
  "model": "urn:air:sd1:checkpoint:civitai:4384@128713",
  "prompt": "a beautiful sunset over mountains",
  "width": 512,
  "height": 512
}
```

5. **VS Code will pause** at your breakpoint! Now you can:
   - Inspect variables (hover over them)
   - Check the call stack
   - Step through code (F10 = step over, F11 = step into)
   - Evaluate expressions in the Debug Console

### Common Breakpoint Locations

```python
# src/mcp/server.py
@mcp.tool()
async def generate_image(...):
    # Line 45: Check incoming parameters
    request = GenerateImageRequest(...)  # <-- Breakpoint here
    
    # Line 57: Check before API call
    result = await service.generate_and_download(...)  # <-- Breakpoint here
    
    # Line 64: Check the result
    image_b64 = base64.b64encode(result['image_data'])  # <-- Breakpoint here
```

```python
# src/core/services/civitai_service.py
async def generate_and_download(self, request, timeout, poll_interval):
    # Add breakpoints to debug API interactions
    response = await self._submit_job(request)  # <-- API submission
    result = await self._poll_job(token, timeout, poll_interval)  # <-- Polling
```

## Environment Variables

Make sure your `.env` file exists with:
```env
CIVITAI_API_TOKEN=your_token_here
```

The debug configurations will automatically load it.

## Troubleshooting

### Inspector Can't Connect
- Make sure the MCP server is running in debug mode first
- Check that you're using the correct Python interpreter (`.venv/bin/python`)
- Verify environment variables are loaded

### Breakpoints Not Hitting
- Ensure "justMyCode" is set to `false` in launch.json (already configured)
- Check that you saved the file with breakpoints
- Verify the code is actually being executed

### Import Errors
- Run `uv sync` to ensure all dependencies are installed
- Check that `PYTHONPATH` includes workspace folder
- Verify you're using the virtual environment Python

### Timeout Issues
- The default timeout is 300 seconds
- For debugging, you might want to increase it
- Or use a faster model for testing

## Advanced Debugging

### Debug with Conditional Breakpoints

Right-click on a breakpoint > Edit Breakpoint > Add condition:
```python
prompt == "test"  # Only break when prompt is "test"
```

### Debug Console Commands

While paused at a breakpoint, try these in the Debug Console:

```python
# Inspect variables
print(request)
print(request.model)

# Evaluate expressions
len(prompt)
request.__dict__

# Call functions
import json
json.dumps(request.__dict__, indent=2)
```

### Log Points (Non-Breaking Breakpoints)

Right-click line > Add Logpoint:
```
Request: {request}, Model: {request.model}
```

This logs without stopping execution - great for production debugging!

## Testing Different Scenarios

### Test 1: Basic Image Generation
```json
{
  "model": "urn:air:sd1:checkpoint:civitai:4384@128713",
  "prompt": "a serene landscape",
  "width": 512,
  "height": 512
}
```

### Test 2: With Negative Prompt
```json
{
  "model": "urn:air:sd1:checkpoint:civitai:4384@128713",
  "prompt": "a beautiful portrait",
  "negative_prompt": "blurry, bad quality",
  "width": 768,
  "height": 768,
  "steps": 30,
  "cfg_scale": 8.5
}
```

### Test 3: With Seed (Reproducible)
```json
{
  "model": "urn:air:sd1:checkpoint:civitai:4384@128713",
  "prompt": "a futuristic city",
  "seed": 42,
  "width": 1024,
  "height": 512
}
```

## Performance Profiling

To profile your MCP server:

1. Install profiling tools:
```bash
uv add --dev py-spy
```

2. Run with profiling:
```bash
py-spy record -o profile.svg -- python -m src.mcp.main
```

3. Use inspector to trigger tools, then view `profile.svg`

## Tips

- 🎯 **Use logging liberally** - especially for async operations
- 🔍 **Watch the Variables pane** - it auto-updates as you step through
- 🚀 **Test with quick models first** - debug logic before waiting for slow generations
- 📝 **Keep a test cases file** - save your JSON test inputs for repeated testing
- 🐛 **Check the MCP Inspector's Network tab** - see the JSON-RPC messages

## Resources

- [VS Code Python Debugging](https://code.visualstudio.com/docs/python/debugging)
- [MCP Inspector Docs](https://github.com/modelcontextprotocol/inspector)
- [Python debugpy](https://github.com/microsoft/debugpy)

---

Happy debugging! 🐛🔧

