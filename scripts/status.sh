#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Persona Generation System Status${NC}"
echo "================================"

# Check virtual environment
echo -n "Virtual Environment: "
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ Installed${NC}"
else
    echo -e "${RED}✗ Not found${NC}"
fi

# Check ComfyUI
echo -n "ComfyUI: "
if [ -d "ComfyUI" ]; then
    echo -e "${GREEN}✓ Installed${NC}"
else
    echo -e "${RED}✗ Not installed${NC}"
fi

# Check SD Scripts
echo -n "SD Training Scripts: "
if [ -d "sd-scripts" ]; then
    echo -e "${GREEN}✓ Installed${NC}"
else
    echo -e "${RED}✗ Not installed${NC}"
fi

# Check models
echo ""
echo "Models:"
if [ -d "models/checkpoints" ]; then
    checkpoint_count=$(find models/checkpoints -name "*.safetensors" -o -name "*.ckpt" | wc -l | tr -d ' ')
    echo "  Checkpoints: $checkpoint_count"
fi
if [ -d "models/loras" ]; then
    lora_count=$(find models/loras -name "*.safetensors" | wc -l | tr -d ' ')
    echo "  LoRAs: $lora_count"
fi

# Check training data
echo ""
echo "Training Data:"
if [ -d "training_data/raw" ]; then
    raw_count=$(find training_data/raw -name "*.jpg" -o -name "*.png" -o -name "*.jpeg" | wc -l | tr -d ' ')
    echo "  Raw images: $raw_count"
fi
if [ -d "training_data/processed" ]; then
    processed_count=$(find training_data/processed -name "*.png" | wc -l | tr -d ' ')
    echo "  Processed images: $processed_count"
fi

# Check outputs
echo ""
echo "Outputs:"
if [ -d "outputs/images" ]; then
    image_count=$(find outputs/images -name "*.png" -o -name "*.jpg" | wc -l | tr -d ' ')
    echo "  Generated images: $image_count"
fi
if [ -d "outputs/videos" ]; then
    video_count=$(find outputs/videos -name "*.mp4" -o -name "*.avi" | wc -l | tr -d ' ')
    echo "  Generated videos: $video_count"
fi

# System info
echo ""
echo "System Info:"
echo "  macOS: $(sw_vers -productVersion)"
echo "  Chip: $(sysctl -n machdep.cpu.brand_string)"
echo "  Memory: $(sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}')"

# Python info
if [ -f "venv/bin/python" ]; then
    echo "  Python: $(venv/bin/python --version)"
    if venv/bin/python -c "import torch; print(f'  PyTorch: {torch.__version__}')" 2>/dev/null; then
        venv/bin/python -c "import torch; print(f'  MPS Available: {torch.backends.mps.is_available()}')"
    fi
fi

echo ""
echo -e "${BLUE}Quick Commands:${NC}"
echo "  Setup: ./quickstart.sh"
echo "  Train: ./scripts/train_lora.sh PERSONA_NAME"
echo "  Run UI: ./scripts/run_comfyui.sh"
echo "  CLI: python persona_gen.py --help"
