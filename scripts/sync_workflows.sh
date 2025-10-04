#!/bin/bash

# Sync workflows to ComfyUI
# This ensures workflows appear in ComfyUI's workflow browser

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if ComfyUI exists
if [ ! -d "${PROJECT_ROOT}/ComfyUI" ]; then
    echo "Error: ComfyUI not found. Run setup.sh first."
    exit 1
fi

# Create ComfyUI workflows directory if it doesn't exist
COMFYUI_WORKFLOWS="${PROJECT_ROOT}/ComfyUI/user/default/workflows"
mkdir -p "$COMFYUI_WORKFLOWS"

# Sync workflows
if [ -d "${PROJECT_ROOT}/workflows" ]; then
    echo "Syncing workflows to ComfyUI..."
    cp -v "${PROJECT_ROOT}/workflows"/*.json "$COMFYUI_WORKFLOWS/" 2>/dev/null || echo "No workflows found to sync"
    echo "✓ Workflows synced to ComfyUI"
else
    echo "No workflows directory found"
fi

# Sync models to ComfyUI
echo "Syncing models to ComfyUI..."
if [ -d "${PROJECT_ROOT}/models/checkpoints" ]; then
    cp -v "${PROJECT_ROOT}/models/checkpoints"/*.safetensors "${PROJECT_ROOT}/ComfyUI/models/checkpoints/" 2>/dev/null || echo "No checkpoints found"
    echo "✓ Checkpoints synced"
fi

if [ -d "${PROJECT_ROOT}/models/loras" ]; then
    cp -v "${PROJECT_ROOT}/models/loras"/*.safetensors "${PROJECT_ROOT}/ComfyUI/models/loras/" 2>/dev/null || echo "No LoRAs found"
    echo "✓ LoRAs synced"
fi

if [ -d "${PROJECT_ROOT}/models/vaes" ]; then
    cp -v "${PROJECT_ROOT}/models/vaes"/*.safetensors "${PROJECT_ROOT}/ComfyUI/models/vae/" 2>/dev/null || echo "No VAEs found"
fi

if [ -d "${PROJECT_ROOT}/models/controlnet" ]; then
    cp -v "${PROJECT_ROOT}/models/controlnet"/*.safetensors "${PROJECT_ROOT}/ComfyUI/models/controlnet/" 2>/dev/null || echo "No ControlNet models found"
fi

echo ""
echo "✓ All models and workflows synced to ComfyUI!"
echo "Workflows are now available in ComfyUI's workflow browser"
