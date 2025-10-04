#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
source "${PROJECT_ROOT}/.env"

# Model URLs
SDXL_BASE_URL="https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors"
SDXL_REFINER_URL="https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors"
SDXL_VAE_URL="https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl_vae.safetensors"
ANIMATEDIFF_URL="https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v2.ckpt"
CONTROLNET_OPENPOSE_URL="https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth"

# Download function with resume support
download_model() {
    local url=$1
    local output_path=$2
    local model_name=$(basename "$output_path")
    
    if [ -f "$output_path" ]; then
        echo "✓ $model_name already exists, skipping..."
        return 0
    fi
    
    echo "Downloading $model_name..."
    mkdir -p "$(dirname "$output_path")"
    
    # Use wget with resume support
    if command -v wget &> /dev/null; then
        wget -c "$url" -O "$output_path"
    else
        # Fallback to curl
        curl -L -C - "$url" -o "$output_path"
    fi
}

echo "Starting model downloads..."

# Download SDXL models
download_model "$SDXL_BASE_URL" "${MODELS_DIR}/checkpoints/sd_xl_base_1.0.safetensors"
download_model "$SDXL_REFINER_URL" "${MODELS_DIR}/checkpoints/sd_xl_refiner_1.0.safetensors"
download_model "$SDXL_VAE_URL" "${MODELS_DIR}/vae/sdxl_vae.safetensors"

# Download AnimateDiff model
download_model "$ANIMATEDIFF_URL" "${MODELS_DIR}/animatediff/mm_sd_v15_v2.ckpt"

# Download ControlNet models
download_model "$CONTROLNET_OPENPOSE_URL" "${MODELS_DIR}/controlnet/control_v11p_sd15_openpose.pth"

echo ""
echo "Model download complete!"
echo "Models are stored in: ${MODELS_DIR}"
