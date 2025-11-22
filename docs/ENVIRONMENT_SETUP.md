# Setting Environment Variables for Debugging

This guide explains how to set the `CIVITAI_API_TOKEN` environment variable for VS Code debugging.

## ✅ Your Setup is Complete!

Your `.env` file has been created with your API token:

```env
CIVITAI_API_TOKEN=efee2e754fc6e34d3cf75f3736f702cb
```

**Security Note:** ✅ The `.env` file is in `.gitignore` and won't be committed to Git.

## 🎯 How to Debug (3 Methods)

### Method 1: Using .env File (Recommended) ⭐

This is the **best and most secure** method.

1. Press `F5` in VS Code
2. Select **"Debug MCP Server (Direct)"**
3. The token is automatically loaded from `.env`

**How it works:**
- The `"envFile"` setting in `launch.json` loads `.env`
- Your token stays secure and isn't committed to Git
- Works for all team members with their own tokens

```json
{
  "envFile": "${workspaceFolder}/.env"
}
```

### Method 2: System Environment Variable

Set it in your shell before opening VS Code:

```bash
# Set for current session
export CIVITAI_API_TOKEN=efee2e754fc6e34d3cf75f3736f702cb

# Then open VS Code
code /home/ofilonenko/Projects/civitai-mcp
```

Or add to your `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export CIVITAI_API_TOKEN=efee2e754fc6e34d3cf75f3736f702cb' >> ~/.bashrc
source ~/.bashrc
```

Then use this debug configuration (already configured):

```json
{
  "env": {
    "CIVITAI_API_TOKEN": "${env:CIVITAI_API_TOKEN}"
  }
}
```

### Method 3: Hardcoded in launch.json

**⚠️ Not recommended for Git repositories** (but I've added it for your convenience)

1. Press `F5`
2. Select **"Debug MCP Server (Hardcoded Token)"**
3. The token is directly in the config

**Only use this if:**
- You're working alone
- The repository is private
- You won't commit `launch.json`

## 📋 Available Debug Configurations

### 1. Debug MCP Server (Direct) ⭐ RECOMMENDED
- Loads from `.env` file
- Fast startup
- Secure

### 2. Debug MCP Server (with uv)
- Loads from `.env` file
- Production-like environment
- Secure

### 3. Debug MCP Server (Hardcoded Token)
- Token directly in config
- Quick for solo development
- ⚠️ Don't commit to Git!

## 🔄 Quick Test

1. **Start debugging:**
   ```bash
   # Press F5 in VS Code
   # OR run:
   cd /home/ofilonenko/Projects/civitai-mcp
   ./scripts/quick_debug.sh
   ```

2. **Verify token is loaded:**
   - Set a breakpoint at line 10 in `src/mcp/server.py`
   - In Debug Console, type: `import os; print(os.getenv('CIVITAI_API_TOKEN'))`
   - You should see: `efee2e754fc6e34d3cf75f3736f702cb`

## 🛠️ Troubleshooting

### Token Not Found

**Symptom:** Error saying `CIVITAI_API_TOKEN` is required

**Solutions:**

1. Check `.env` file exists:
   ```bash
   cat /home/ofilonenko/Projects/civitai-mcp/.env
   ```

2. Reload VS Code window:
   - Press `Ctrl+Shift+P`
   - Type "Reload Window"
   - Press Enter

3. Check the debug configuration includes `"envFile"`:
   ```json
   "envFile": "${workspaceFolder}/.env"
   ```

### Token Loaded but Still Fails

Check that your token is valid:

```bash
curl -H "Authorization: Bearer efee2e754fc6e34d3cf75f3736f702cb" \
     https://civitai.com/api/v1/models
```

If this fails, get a new token from: https://civitai.com/user/account

### .env File Not Loading

Try the hardcoded configuration:
1. Press `F5`
2. Select "Debug MCP Server (Hardcoded Token)"
3. This bypasses `.env` file loading

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Use `.env` file for local development
- ✅ Keep `.env` in `.gitignore`
- ✅ Use environment variables in production
- ✅ Rotate tokens periodically
- ✅ Use different tokens for dev/prod

### ❌ DON'T:
- ❌ Commit `.env` files to Git
- ❌ Share tokens in chat/email
- ❌ Hardcode tokens in source code
- ❌ Use production tokens in development

## 📝 Current Configuration Files

### .env (gitignored)
```env
CIVITAI_API_TOKEN=efee2e754fc6e34d3cf75f3736f702cb
APP_HOST=0.0.0.0
APP_PORT=8000
```

### .vscode/launch.json
Three configurations available:
1. Direct (uses .env)
2. With uv (uses .env)
3. Hardcoded (for quick testing)

## 🎯 Next Steps

1. **Start debugging:** Press `F5`
2. **Launch inspector:** `./scripts/debug_with_inspector.sh`
3. **Set breakpoints:** Line 45, 57, 64 in `src/mcp/server.py`
4. **Test with MCP Inspector:** Use the test cases from `tests/mcp_test_cases.json`

## 🆘 Quick Commands

```bash
# View your .env
cat .env

# Set token in current shell
export CIVITAI_API_TOKEN=efee2e754fc6e34d3cf75f3736f702cb

# Test token works
curl -H "Authorization: Bearer $CIVITAI_API_TOKEN" \
     https://civitai.com/api/v1/models | head -20

# Start debugging
code . && # Opens VS Code, then press F5

# Start inspector (in separate terminal)
./scripts/debug_with_inspector.sh
```

## 📚 Related Documentation

- [Debugging Guide](DEBUGGING.md) - Full debugging workflow
- [Debugging Workflow](DEBUGGING_WORKFLOW.md) - Visual diagrams
- [VS Code Launch Config](.vscode/README.md) - Configuration details

---

Your environment is configured and ready to debug! 🎉

