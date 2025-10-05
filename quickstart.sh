#!/bin/bash
set -euo pipefail

# Quick Start Script - One command to set up everything

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  Persona Generation Quick Start${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Step 1: Run setup
echo -e "${YELLOW}Step 1: Running initial setup...${NC}"
if [ -f "setup.sh" ]; then
    ./setup.sh
else
    echo -e "${RED}Error: setup.sh not found${NC}"
    exit 1
fi

# Step 2: Check if models need downloading
echo ""
echo -e "${YELLOW}Step 2: Checking models...${NC}"
if [ ! -f "models/checkpoints/sd_xl_base_1.0.safetensors" ]; then
    echo "Models not found. Downloading..."
    ./scripts/download_models.sh
else
    echo -e "${GREEN}✓ Models already downloaded${NC}"
fi

# Step 3: Install additional dependencies
echo ""
echo -e "${YELLOW}Step 3: Installing ffmpeg for video processing...${NC}"
if ! command -v ffmpeg &> /dev/null; then
    if command -v brew &> /dev/null; then
        brew install ffmpeg
    else
        echo -e "${YELLOW}Please install ffmpeg manually for video processing${NC}"
    fi
else
    echo -e "${GREEN}✓ ffmpeg already installed${NC}"
fi

# Step 4: Create example training data directory
echo ""
echo -e "${YELLOW}Step 4: Setting up example directories...${NC}"
mkdir -p training_data/raw
mkdir -p training_data/processed
echo "Place your persona images in: training_data/raw/" > training_data/raw/README.txt

# Step 5: Create example persona and directories
echo ""
echo -e "${YELLOW}Step 5: Setting up example persona...${NC}"
source venv/bin/activate

# Check if personas.json exists, if not create example persona
if [ ! -f "personas.json" ]; then
    python scripts/persona_manager.py add --name "Example Person" --description "Example persona for testing"
    echo -e "${GREEN}✓ Created example persona: persona-example_person${NC}"
else
    echo -e "${GREEN}✓ Personas already configured${NC}"
fi

# Final message
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}    Setup Complete! 🎉${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${BLUE}Quick Test:${NC}"
echo "${YELLOW}python test_setup.py${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Create a persona: ${YELLOW}python scripts/persona_manager.py add --name 'Your Name'${NC}"
echo "2. Add 20-30 images to: ${YELLOW}training_data/persona-your_name/raw/${NC}"
echo "3. Process images: ${YELLOW}python scripts/prepare_training_data.py --persona-id persona-your_name${NC}"
echo "4. Train LoRA: ${YELLOW}./scripts/train_lora.sh persona-your_name${NC}"
echo "5. Start ComfyUI: ${YELLOW}./scripts/run_comfyui.sh${NC}"
echo ""
echo -e "${BLUE}For multiple personas:${NC}"
echo "${YELLOW}python scripts/persona_manager.py --help${NC}"
echo ""
echo -e "${GREEN}Happy persona generating! 🚀${NC}"
