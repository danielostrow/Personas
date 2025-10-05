#!/bin/bash

# Complete validation setup for maximum persona realism
set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <persona-id>"
    echo "Example: $0 persona-saramillie"
    exit 1
fi

PERSONA_ID="$1"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🎯 Complete Validation Setup for Maximum Realism"
echo "================================================"
echo "Persona: $PERSONA_ID"
echo ""

# Activate virtual environment
source "${PROJECT_ROOT}/venv/bin/activate"

# Step 1: Setup validation models
echo "📥 Step 1: Setting up validation models..."
"${SCRIPT_DIR}/setup_validation_models.sh"

# Step 2: Create validation workflows
echo ""
echo "🔍 Step 2: Creating validation workflows..."

# Simple validation workflow
python "${SCRIPT_DIR}/create_simple_validation_workflow.py" \
    --persona-id "$PERSONA_ID" --lora-strength 0.7

echo ""

# Advanced validation workflow  
python "${SCRIPT_DIR}/create_advanced_validation_workflow.py" \
    --persona-id "$PERSONA_ID" --lora-strength 0.65

echo ""

# Step 3: Create strength testing workflows
echo "🧪 Step 3: Creating LoRA strength testing workflows..."
python "${SCRIPT_DIR}/test_lora_strengths.py" \
    --persona-id "$PERSONA_ID" \
    --strengths "0.6,0.65,0.7,0.75,0.8" \
    --prompt "RAW photograph, professional portrait of ${PERSONA_ID}, photorealistic, detailed facial features, natural lighting, 85mm lens"

echo ""
echo "✅ Complete validation setup finished!"
echo ""
echo "🎯 Available Validation Workflows:"
echo "================================="
echo ""
echo "1. 🔍 ${PERSONA_ID}_photorealistic_validation"
echo "   • 2 sampling methods + upscaling"
echo "   • Best for quick quality comparison"
echo ""  
echo "2. 🏆 ${PERSONA_ID}_advanced_validation"
echo "   • 3 sampling methods + comprehensive validation"
echo "   • Maximum quality with professional photography simulation"
echo ""
echo "3. 🧪 ${PERSONA_ID}_strength_X.X_test (5 workflows)"
echo "   • Test different LoRA strengths (0.6 to 0.8)"
echo "   • Find optimal strength for your persona"
echo ""
echo "🎨 Next Steps:"
echo "=============="
echo ""
echo "1. 🚀 Start ComfyUI:"
echo "   ./scripts/restart_comfyui.sh"
echo ""
echo "2. 🔍 Load a validation workflow and run it"
echo ""
echo "3. 📊 Compare results:"
echo "   • Look for natural skin texture"
echo "   • Check for realistic lighting"
echo "   • Ensure no AI artifacts"
echo "   • Verify facial feature accuracy"
echo ""
echo "4. 📝 Document best settings:"
echo "   • Which LoRA strength works best?"
echo "   • Which sampling method is most realistic?"
echo "   • Which CFG scale gives natural results?"
echo ""
echo "5. 🎯 Optional: Retrain with optimized settings"
echo "   ./scripts/quick_improve_persona.sh $PERSONA_ID"
echo ""
echo "📖 For detailed guidance: docs/IMPROVING_PERSONA_QUALITY.md"
