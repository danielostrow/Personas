#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
source "${PROJECT_ROOT}/.env"
source "${VENV_DIR}/bin/activate"

# Training parameters
PERSONA_ID="${1:-}"
LEARNING_RATE="${2:-1e-4}"
TRAIN_STEPS="${3:-4000}"
BATCH_SIZE="${4:-1}"  # Lower batch size for M4 Mac memory

# Check if persona ID provided
if [ -z "$PERSONA_ID" ]; then
    echo "Error: Please provide a persona ID (e.g., persona-john)"
    echo "Usage: $0 <persona-id> [learning-rate] [train-steps] [batch-size]"
    exit 1
fi

# Get persona info
PERSONA_INFO=$(python -c "
from pathlib import Path
import sys
sys.path.insert(0, '${SCRIPT_DIR}')
from persona_manager import PersonaManager
manager = PersonaManager(Path('${PROJECT_ROOT}'))
persona = manager.get_persona('${PERSONA_ID}')
if persona:
    print(f\"{persona['name']}|{persona['trigger_word']}|{persona['training_data_path']}\")
else:
    print('NOT_FOUND')
")

if [ "$PERSONA_INFO" = "NOT_FOUND" ]; then
    echo "Error: Persona ${PERSONA_ID} not found"
    echo "Use: python scripts/persona_manager.py add --name 'Your Name'"
    exit 1
fi

IFS='|' read -r PERSONA_NAME TRIGGER_WORD TRAIN_DATA_PATH <<< "$PERSONA_INFO"

# Paths
BASE_MODEL="${MODELS_DIR}/checkpoints/sd_xl_base_1.0.safetensors"
OUTPUT_DIR="${OUTPUTS_DIR}/${PERSONA_ID}_lora_$(date +%Y%m%d_%H%M%S)"
CONFIG_FILE="${PROJECT_ROOT}/configs/${PERSONA_ID}_lora_config.toml"

# Validate inputs
if [ ! -f "$BASE_MODEL" ]; then
    echo "Error: Base model not found. Run ./scripts/download_models.sh first."
    exit 1
fi

if [ ! -d "$TRAIN_DATA_PATH" ] || [ -z "$(ls -A "$TRAIN_DATA_PATH"/10_* 2>/dev/null)" ]; then
    echo "Error: No training data found in ${TRAIN_DATA_PATH}"
    echo "Please prepare your training data first"
    exit 1
fi

# Create LoRA config
cat > "$CONFIG_FILE" << EOF
[model_arguments]
v2 = false
v_parameterization = false
pretrained_model_name_or_path = "${BASE_MODEL}"

[additional_network_arguments]
network_module = "networks.lora"
network_dim = 64
network_alpha = 32

[optimizer_arguments]
optimizer_type = "AdamW"
learning_rate = ${LEARNING_RATE}
lr_scheduler = "cosine_with_restarts"
lr_warmup_steps = 500

[dataset_arguments]
train_data_dir = "${TRAIN_DATA_PATH}"
resolution = "1024,1024"
batch_size = ${BATCH_SIZE}
caption_extension = ".txt"
keep_tokens = 1
enable_bucket = true

[training_arguments]
output_dir = "${OUTPUT_DIR}"
output_name = "${PERSONA_ID}"
save_model_as = "safetensors"
save_every_n_epochs = 5
max_train_steps = ${TRAIN_STEPS}
gradient_checkpointing = true
mixed_precision = "no"
xformers = false
clip_skip = 1
seed = 42
logging_dir = "${OUTPUT_DIR}/logs"

[sample_prompt_arguments]
sample_every_n_epochs = 5
sample_prompts = "${PROJECT_ROOT}/configs/${PERSONA_ID}_sample_prompts.txt"
EOF

# Create sample prompts
cat > "${PROJECT_ROOT}/configs/${PERSONA_ID}_sample_prompts.txt" << EOF
masterpiece, best quality, 1girl, ${TRIGGER_WORD}, portrait, looking at viewer --n low quality, bad anatomy, blurry
masterpiece, best quality, 1girl, ${TRIGGER_WORD}, full body, standing, casual outfit --n low quality, bad anatomy, blurry
masterpiece, best quality, 1girl, ${TRIGGER_WORD}, upper body, smile, outdoors --n low quality, bad anatomy, blurry
EOF

echo "Starting LoRA training for: ${PERSONA_NAME}"
echo "Output will be saved to: ${OUTPUT_DIR}"
echo ""

# Run training
cd "${SD_SCRIPTS_DIR}"
accelerate launch sdxl_train_network.py \
    --config_file "$CONFIG_FILE" \
    --enable_bucket \
    --min_bucket_reso 256 \
    --max_bucket_reso 2048 \
    --bucket_reso_steps 64

# Copy final model to loras directory
LORA_FILE="${PERSONA_ID}.safetensors"
if [ -f "${OUTPUT_DIR}/${LORA_FILE}" ]; then
    cp "${OUTPUT_DIR}/${LORA_FILE}" "${MODELS_DIR}/loras/"
    
    # Update persona manager
    python -c "
from pathlib import Path
import sys
sys.path.insert(0, '${SCRIPT_DIR}')
from persona_manager import PersonaManager
manager = PersonaManager(Path('${PROJECT_ROOT}'))
manager.mark_trained('${PERSONA_ID}', '${LORA_FILE}')
"
    
    echo ""
    echo "Training complete! LoRA saved to:"
    echo "${MODELS_DIR}/loras/${LORA_FILE}"
    echo ""
    echo "Trigger word: ${TRIGGER_WORD}"
    echo ""
    echo "To use this persona in prompts, use: ${TRIGGER_WORD}"
    echo "Example: 'masterpiece, ${TRIGGER_WORD} wearing a suit, professional photo'"
else
    echo "Error: Training failed or output not found"
    exit 1
fi
