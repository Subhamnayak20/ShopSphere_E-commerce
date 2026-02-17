# Virtual Environment Setup Guide

## Current Status

✅ **Virtual environment already exists** at: `.venv/`

## Activating the Virtual Environment

### Windows (PowerShell)
```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)
```cmd
.venv\Scripts\activate.bat
```

### Linux/macOS
```bash
source .venv/bin/activate
```

### Git Bash (Windows)
```bash
source .venv/Scripts/activate
```

## Verifying Virtual Environment

After activation, you should see `(.venv)` prefix in your terminal:
```
(.venv) PS C:\Users\HP\ShopSphere_E-commerce>
```

Check Python location:
```bash
# Should point to .venv directory
python -c "import sys; print(sys.executable)"
```

## Installing Dependencies

With virtual environment activated:
```bash
pip install -r requirements.txt
```

## Deactivating Virtual Environment

```bash
deactivate
```

## Creating New Virtual Environment (If Needed)

If you need to recreate the virtual environment:

### Windows
```powershell
# Remove old environment
Remove-Item -Recurse -Force .venv

# Create new environment
python -m venv .venv


# Activate
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Linux/macOS
```bash
# Remove old environment
rm -rf .venv

# Create new environment
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running Services with Virtual Environment

### Option 1: Activate First (Recommended)
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run services
uvicorn product_service:app --reload --port 8000
uvicorn user_service:app --reload --port 8001
uvicorn order_service:app --reload --port 8002
```

### Option 2: Direct Execution
```bash
# Windows
.\.venv\Scripts\python.exe -m uvicorn product_service:app --reload --port 8000

# Linux/macOS
./.venv/bin/python -m uvicorn product_service:app --reload --port 8000
```

## Benefits of Virtual Environment

✅ **Isolation**: Dependencies don't conflict with system Python
✅ **Reproducibility**: Same environment across different machines
✅ **Clean**: Easy to delete and recreate
✅ **Version Control**: Can have different Python versions per project

## Checking Installed Packages

```bash
# List all installed packages
pip list

# Show specific package
pip show fastapi

# Export current packages
pip freeze > requirements.txt
```

## Troubleshooting

### Issue: Cannot activate (PowerShell execution policy)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Wrong Python version
```bash
# Check Python version
python --version

# Create venv with specific Python version
py -3.11 -m venv .venv
```

### Issue: Missing packages
```bash
# Activate venv first
.\.venv\Scripts\Activate.ps1

# Install all dependencies
pip install -r requirements.txt
```

## Docker Note

When using Docker, the virtual environment is **not needed** because:
- Docker containers have isolated Python environments
- Dependencies are installed in the container image
- Each container is already isolated

## IDE Configuration

### VS Code
Add to `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": ".venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true
}
```

### PyCharm
1. File → Settings → Project → Python Interpreter
2. Add Interpreter → Existing Environment
3. Select: `.venv/Scripts/python.exe`

## Best Practices

1. ✅ Always activate venv before running services locally
2. ✅ Keep `requirements.txt` updated
3. ✅ Add `.venv/` to `.gitignore` (already done)
4. ✅ Use same Python version across team
5. ✅ Document Python version in README

## Quick Commands

```bash
# Activate
.\.venv\Scripts\Activate.ps1

# Check activation
python -c "import sys; print(sys.prefix)"

# Install package
pip install package-name

# Update requirements
pip freeze > requirements.txt

# Deactivate
deactivate
```
