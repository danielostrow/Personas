#!/bin/bash
set -euo pipefail

# Persona Generation Setup Script - Idempotent Installation
# For Apple Silicon (M4) Mac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="persona-gen"
VENV_DIR="${SCRIPT_DIR}/venv"
MODELS_DIR="${SCRIPT_DIR}/models"
OUTPUTS_DIR="${SCRIPT_DIR}/outputs"
TRAINING_DATA_DIR="${SCRIPT_DIR}/training_data"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up Persona Generation Environment${NC}"

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "This script is designed for macOS with Apple Silicon"
    exit 1
fi

# Create project structure
echo "Creating project structure..."
mkdir -p "${MODELS_DIR}"/{checkpoints,loras,controlnet,vae,animatediff}
mkdir -p "${OUTPUTS_DIR}"/{images,videos,processed}
mkdir -p "${TRAINING_DATA_DIR}"/{raw,processed}
mkdir -p "${SCRIPT_DIR}"/{configs,workflows,scripts}

# Create or activate virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

# Upgrade pip
pip install --upgrade pip

# Install PyTorch with MPS support
echo -e "${YELLOW}Installing PyTorch with MPS support...${NC}"
pip install torch torchvision torchaudio

# Clone or update ComfyUI
if [ ! -d "${SCRIPT_DIR}/ComfyUI" ]; then
    echo "Cloning ComfyUI..."
    git clone https://github.com/comfyanonymous/ComfyUI "${SCRIPT_DIR}/ComfyUI"
else
    echo "Updating ComfyUI..."
    cd "${SCRIPT_DIR}/ComfyUI"
    git pull
    cd "$SCRIPT_DIR"
fi

# Install ComfyUI requirements
echo "Installing ComfyUI requirements..."
pip install -r "${SCRIPT_DIR}/ComfyUI/requirements.txt"

# Clone or update training scripts
if [ ! -d "${SCRIPT_DIR}/sd-scripts" ]; then
    echo "Cloning SD training scripts..."
    git clone https://github.com/kohya-ss/sd-scripts.git "${SCRIPT_DIR}/sd-scripts"
else
    echo "Updating SD training scripts..."
    cd "${SCRIPT_DIR}/sd-scripts"
    git pull
    cd "$SCRIPT_DIR"
fi

# Install training requirements
echo "Installing training script requirements..."
pip install -r "${SCRIPT_DIR}/sd-scripts/requirements.txt"
pip install accelerate xformers bitsandbytes

# Install custom nodes for ComfyUI
echo "Installing ComfyUI custom nodes..."
CUSTOM_NODES_DIR="${SCRIPT_DIR}/ComfyUI/custom_nodes"

# AnimateDiff
if [ ! -d "${CUSTOM_NODES_DIR}/ComfyUI-AnimateDiff-Evolved" ]; then
    git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git "${CUSTOM_NODES_DIR}/ComfyUI-AnimateDiff-Evolved"
fi

# ControlNet
if [ ! -d "${CUSTOM_NODES_DIR}/comfyui_controlnet_aux" ]; then
    git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git "${CUSTOM_NODES_DIR}/comfyui_controlnet_aux"
fi

# ComfyUI Manager (for easy node management)
if [ ! -d "${CUSTOM_NODES_DIR}/ComfyUI-Manager" ]; then
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git "${CUSTOM_NODES_DIR}/ComfyUI-Manager"
fi

# Install additional useful tools
echo "Installing additional tools..."
pip install opencv-python pillow numpy matplotlib tqdm rich click

# Create symlinks for models (idempotent)
echo "Setting up model directories..."
ln -sfn "${MODELS_DIR}/checkpoints" "${SCRIPT_DIR}/ComfyUI/models/checkpoints"
ln -sfn "${MODELS_DIR}/loras" "${SCRIPT_DIR}/ComfyUI/models/loras"
ln -sfn "${MODELS_DIR}/controlnet" "${SCRIPT_DIR}/ComfyUI/models/controlnet"
ln -sfn "${MODELS_DIR}/vae" "${SCRIPT_DIR}/ComfyUI/models/vae"

# Create environment file
cat > "${SCRIPT_DIR}/.env" << EOF
PROJECT_ROOT=${SCRIPT_DIR}
VENV_DIR=${VENV_DIR}
MODELS_DIR=${MODELS_DIR}
OUTPUTS_DIR=${OUTPUTS_DIR}
TRAINING_DATA_DIR=${TRAINING_DATA_DIR}
COMFYUI_DIR=${SCRIPT_DIR}/ComfyUI
SD_SCRIPTS_DIR=${SCRIPT_DIR}/sd-scripts
EOF

echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Download models using: ./scripts/download_models.sh"
echo "2. Prepare training data in: ${TRAINING_DATA_DIR}/raw"
echo "3. Train your LoRA using: ./scripts/train_lora.sh"
echo "4. Run ComfyUI: ./scripts/run_comfyui.sh"
