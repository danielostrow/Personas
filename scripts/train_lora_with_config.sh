#!/bin/bash

# Train LoRA with custom config file
set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <config_file.toml>"
    echo "Example: $0 configs/persona-saramillie_optimized_config.toml"
    exit 1
fi

CONFIG_FILE="$1"

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file not found: $CONFIG_FILE"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SD_SCRIPTS_DIR="${PROJECT_ROOT}/sd-scripts"

# Activate virtual environment
source "${PROJECT_ROOT}/venv/bin/activate"

# Check if sd-scripts exists
if [ ! -d "$SD_SCRIPTS_DIR" ]; then
    echo "Error: sd-scripts not found. Run setup.sh first."
    exit 1
fi

echo "🚀 Starting LoRA training with custom config..."
echo "📋 Config file: $CONFIG_FILE"
echo ""

# Run training
cd "$SD_SCRIPTS_DIR"
accelerate launch sdxl_train_network.py \
    --config_file "$CONFIG_FILE" \
    --enable_bucket \
    --min_bucket_reso 512 \
    --max_bucket_reso 2048 \
    --bucket_reso_steps 64

TRAINING_EXIT_CODE=$?

if [ $TRAINING_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Training completed successfully!"
    
    # Get output info from config
    OUTPUT_DIR=$(grep 'output_dir = ' "$CONFIG_FILE" | cut -d'"' -f2)
    OUTPUT_NAME=$(grep 'output_name = ' "$CONFIG_FILE" | cut -d'"' -f2)
    
    # Copy LoRA to models directory
    if [ -f "${OUTPUT_DIR}/${OUTPUT_NAME}.safetensors" ]; then
        cp "${OUTPUT_DIR}/${OUTPUT_NAME}.safetensors" "${PROJECT_ROOT}/models/loras/"
        echo "📁 LoRA copied to: models/loras/${OUTPUT_NAME}.safetensors"
        
        # Update persona manager if this is an optimized training
        if [[ "$OUTPUT_NAME" == *"_optimized" ]]; then
            PERSONA_ID=$(echo "$OUTPUT_NAME" | sed 's/_optimized$//')
            python "${PROJECT_ROOT}/scripts/persona_manager.py" mark-trained "$PERSONA_ID" \
                --lora-file "models/loras/${OUTPUT_NAME}.safetensors" 2>/dev/null || echo "Could not update persona registry"
        fi
    fi
    
    echo ""
    echo "🎯 Next steps:"
    echo "1. Test different LoRA strengths:"
    echo "   python persona_gen.py create-workflow --persona-id <persona> --type image"
    echo "2. Generate comparison images:"
    echo "   python scripts/test_lora_strengths.py --persona-id <persona>"
    
else
    echo ""
    echo "❌ Training failed with exit code: $TRAINING_EXIT_CODE"
    echo "Check the logs above for details."
    exit $TRAINING_EXIT_CODE
fi
