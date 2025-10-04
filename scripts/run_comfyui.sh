#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
source "${PROJECT_ROOT}/.env"
source "${VENV_DIR}/bin/activate"

# ComfyUI settings
PORT="${1:-8188}"
LISTEN="${2:-127.0.0.1}"

echo "Starting ComfyUI on http://${LISTEN}:${PORT}"
echo "Press Ctrl+C to stop"
echo ""

# Change to ComfyUI directory
cd "${COMFYUI_DIR}"

# Run ComfyUI with optimized settings for M4 Mac
python main.py \
    --listen "${LISTEN}" \
    --port "${PORT}" \
    --preview-method auto \
    --use-pytorch-cross-attention
