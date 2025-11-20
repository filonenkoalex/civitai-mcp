# Simplified Architecture - Single Endpoint/Tool

## Overview

Streamlined implementation with a single endpoint and single MCP tool that:
1. Takes all generation parameters as input
2. Waits for completion
3. Returns the actual image (MCP) or metadata/binary (API)

## Architecture

```
┌─────────────────────────────────────────┐
│          Single Interface Point          │
│                                          │
│  API: POST /generate                    │
│  MCP: generate_image tool               │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│         Core Service                    │
│  generate_and_download()                │
│  1. Submit job                          │
│  2. Poll until complete                 │
│  3. Download image                      │
│  4. Return image data + metadata        │
└─────────────────────────────────────────┘
```

## Key Features

### ✅ Single Responsibility
- **One endpoint**: `POST /generate`
- **One MCP tool**: `generate_image`
- **One service method**: `generate_and_download()`

### ✅ Complete Flow
```
Input (params) → Generate → Wait → Download → Output (image)
```

### ✅ Clean Service Layer
```python
# src/core/services/civitai_service.py
async def generate_and_download(request, timeout, poll_interval):
    """
    All-in-one method:
    1. Generate image job
    2. Poll for completion
    3. Download image bytes
    4. Return {image_data, seed, metadata}
    """
```

## API Endpoint

### POST /generate

**Input:**
```json
{
  "model": "urn:air:sd1:checkpoint:civitai:4384@128713",
  "prompt": "a serene mountain landscape",
  "width": 512,
  "height": 512,
  "negative_prompt": "blurry",
  "steps": 20,
  "cfg_scale": 7.0,
  "seed": null,
  "timeout": 300,
  "return_image": false
}
```

**Output (return_image=false):**
```json
{
  "success": true,
  "job_id": "...",
  "seed": 123456,
  "cost": 0.64,
  "blob_url": "https://...",
  "prompt": "...",
  "model": "...",
  "message": "Image generated successfully..."
}
```

**Output (return_image=true):**
- Binary image data (image/png)
- Headers: X-Seed, X-Cost, X-Job-ID

## MCP Tool

### generate_image

**Input:**
```json
{
  "model": "urn:air:sd1:checkpoint:civitai:4384@128713",
  "prompt": "a serene mountain landscape",
  "width": 512,
  "height": 512,
  "negative_prompt": "blurry",
  "steps": 20,
  "cfg_scale": 7.0,
  "seed": null,
  "timeout": 300
}
```

**Output:**
```
[
  TextContent("Image generated successfully!\nPrompt: ...\nSeed: ..."),
  ImageContent(data=base64_image, mimeType="image/png")
]
```

## File Structure

```
src/
├── api/
│   ├── main.py              # FastAPI app
│   ├── dependencies.py      # DI
│   └── routes/
│       ├── health.py        # Health check
│       └── generate.py      # Single generation endpoint
├── mcp/
│   ├── main.py              # MCP entry point
│   ├── server.py            # Server setup
│   └── tools/
│       └── generate_image.py  # Single tool
└── core/
    ├── services/
    │   └── civitai_service.py  # generate_and_download()
    ├── contracts/
    │   ├── requests.py       # GenerateImageRequest
    │   └── responses.py      # Response DTOs
    └── config/
        └── settings.py       # Configuration
```

## Benefits

### 1. Simplicity
- ✅ Single entry point per interface
- ✅ No complexity of multiple endpoints/tools
- ✅ Clear, linear flow

### 2. User Experience
- ✅ One call gets you the image
- ✅ No need to poll manually
- ✅ Direct image result

### 3. Maintainability
- ✅ One service method to maintain
- ✅ Clear responsibility
- ✅ Easy to test

### 4. Flexibility
- **API**: Can return JSON metadata or binary image
- **MCP**: Returns actual image using ImageContent
- **Service**: Reusable for both interfaces

## Usage Examples

### MCP (Claude Desktop)

```
"Generate an image of a sunset over mountains using Realistic Vision"

→ Claude calls generate_image tool
→ Tool waits for completion
→ Returns image directly in chat
```

### API (curl)

```bash
# Get metadata + blob URL
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "urn:air:sd1:checkpoint:civitai:4384@128713",
    "prompt": "sunset over mountains"
  }'

# Get actual image binary
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "urn:air:sd1:checkpoint:civitai:4384@128713",
    "prompt": "sunset over mountains",
    "return_image": true
  }' > image.png
```

## Comparison

### Before (Complex)
- ❌ 3 API endpoints (generate, status, jobs)
- ❌ 3 MCP tools (generate, check_status, generate_and_wait)
- ❌ Multiple service methods
- ❌ Manual polling required
- ❌ Complex flow

### After (Simple)
- ✅ 1 API endpoint (generate)
- ✅ 1 MCP tool (generate_image)
- ✅ 1 service method (generate_and_download)
- ✅ Automatic waiting
- ✅ Direct results

## Success Criteria

- [x] Single endpoint per interface
- [x] All parameters supported
- [x] Automatic waiting for completion
- [x] Direct image delivery
- [x] MCP uses ImageContent pattern
- [x] Clean, reusable service layer
- [x] Simple, clear code
- [x] Easy to understand and maintain

Perfect for focused, single-purpose image generation! 🎯
