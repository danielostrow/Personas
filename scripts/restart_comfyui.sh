#!/bin/bash

# Restart ComfyUI to clear cache and reload workflows
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🔄 Restarting ComfyUI to clear cache..."

# Kill any existing ComfyUI processes
pkill -f "python.*main.py" 2>/dev/null || echo "No existing ComfyUI processes found"
pkill -f "ComfyUI" 2>/dev/null || echo "No ComfyUI processes found"

# Wait a moment
sleep 2

# Clear any temp files
if [ -d "${PROJECT_ROOT}/ComfyUI/temp" ]; then
    rm -f "${PROJECT_ROOT}/ComfyUI/temp"/* 2>/dev/null || true
    echo "✓ Cleared temp files"
fi

# Sync models and workflows
echo "📦 Syncing models and workflows..."
"${SCRIPT_DIR}/sync_workflows.sh"

echo ""
echo "🚀 Starting ComfyUI..."
cd "${PROJECT_ROOT}/ComfyUI"
source "${PROJECT_ROOT}/venv/bin/activate"
python main.py --listen 0.0.0.0 &

echo ""
echo "✅ ComfyUI is starting up!"
echo "🌐 Open http://localhost:8188 in your browser"
echo "📋 Your workflows should now be available in the workflow browser"
echo ""
echo "To stop ComfyUI later, run: pkill -f 'python.*main.py'"
