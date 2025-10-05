#!/bin/bash

# Download and setup models needed for validation workflow
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
UPSCALE_DIR="${PROJECT_ROOT}/ComfyUI/models/upscale_models"

echo "🔍 Setting up validation models for realism enhancement..."
echo "=================================================="

# Create upscale models directory
mkdir -p "$UPSCALE_DIR"

# Download RealESRGAN upscaling model for detail enhancement
if [ ! -f "${UPSCALE_DIR}/RealESRGAN_x2plus.pth" ]; then
    echo "📥 Downloading RealESRGAN x2 upscaling model..."
    curl -L "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth" \
         -o "${UPSCALE_DIR}/RealESRGAN_x2plus.pth"
    echo "✅ RealESRGAN x2 model downloaded"
else
    echo "✅ RealESRGAN x2 model already exists"
fi

# Download RealESRGAN x4 for higher quality upscaling
if [ ! -f "${UPSCALE_DIR}/RealESRGAN_x4plus.pth" ]; then
    echo "📥 Downloading RealESRGAN x4 upscaling model..."
    curl -L "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth" \
         -o "${UPSCALE_DIR}/RealESRGAN_x4plus.pth"
    echo "✅ RealESRGAN x4 model downloaded"
else
    echo "✅ RealESRGAN x4 model already exists"
fi

# Download LDSR upscaling model (alternative)
if [ ! -f "${UPSCALE_DIR}/LDSR.safetensors" ] && [ "$1" = "--full" ]; then
    echo "📥 Downloading LDSR upscaling model (optional)..."
    curl -L "https://heibox.uni-heidelberg.de/f/578df07c8fc04ffbadf3/?dl=1" \
         -o "${UPSCALE_DIR}/LDSR.safetensors"
    echo "✅ LDSR model downloaded"
fi

echo ""
echo "✅ Validation models setup complete!"
echo ""
echo "📋 Available upscaling models:"
echo "  • RealESRGAN_x2plus.pth - 2x upscaling, good for faces"
echo "  • RealESRGAN_x4plus.pth - 4x upscaling, maximum detail"
if [ "$1" = "--full" ]; then
    echo "  • LDSR.safetensors - Alternative upscaling method"
fi
echo ""
echo "🎯 Next step: Create validation workflow"
echo "python scripts/create_validation_workflow.py --persona-id your-persona-id"
