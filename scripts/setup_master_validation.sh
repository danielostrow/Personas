#!/bin/bash

# Setup complete master validation system
set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <persona-id>"
    echo "Example: $0 persona-saramillie"
    exit 1
fi

PERSONA_ID="$1"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🎛️ Master Validation System Setup"
echo "================================="
echo "Persona: $PERSONA_ID"
echo ""

# Activate virtual environment
source "${PROJECT_ROOT}/venv/bin/activate"

# Step 1: Setup validation models
echo "📥 Step 1: Setting up validation models..."
"${SCRIPT_DIR}/setup_validation_models.sh"

echo ""

# Step 2: Create the UI-controlled master workflow
echo "🎛️ Step 2: Creating UI-controlled master workflow..."
python "${SCRIPT_DIR}/create_ui_controlled_workflow.py" --persona-id "$PERSONA_ID"

echo ""

# Step 3: Create backup individual workflows (optional)
echo "📋 Step 3: Creating backup individual workflows..."
python "${SCRIPT_DIR}/create_simple_validation_workflow.py" --persona-id "$PERSONA_ID" --lora-strength 0.65

echo ""

# Step 4: Sync everything to ComfyUI
echo "🔄 Step 4: Syncing to ComfyUI..."
"${SCRIPT_DIR}/sync_workflows.sh"

echo ""
echo "✅ Master Validation System Setup Complete!"
echo "=========================================="
echo ""
echo "🎛️ MAIN WORKFLOW (Use This):"
echo "   📋 ${PERSONA_ID}_UI_MASTER_CONTROL"
echo ""
echo "   🎯 Features:"
echo "   • 4 generation methods with different approaches"
echo "   • All settings controllable from ComfyUI interface"
echo "   • 8 output versions (4 original + 4 upscaled)"
echo "   • Easy enable/disable for each method"
echo "   • Comprehensive prompt and LoRA strength controls"
echo ""
echo "🔧 HOW TO USE:"
echo "=============="
echo ""
echo "1. 🚀 Start ComfyUI:"
echo "   ./scripts/restart_comfyui.sh"
echo ""
echo "2. 📋 Load Master Workflow:"
echo "   • Click 'Workflows' → Select '${PERSONA_ID}_UI_MASTER_CONTROL'"
echo ""
echo "3. 🎛️ Configure Options (All in UI):"
echo ""
echo "   a) 🔧 LoRA Strength (Node 2):"
echo "      • Start with: strength_model = 0.65"
echo "      • Try lower (0.6) for more natural look"
echo "      • Try higher (0.7-0.8) for stronger features"
echo ""
echo "   b) 📝 Choose Prompt Style:"
echo "      • Node 4: Photorealistic (RECOMMENDED)"
echo "      • Node 5: Ultra-realistic (Maximum realism)"
echo "      • Node 3: Basic (Simple generations)"
echo ""
echo "   c) 🎨 Enable/Disable Methods:"
echo "      • Method 1 (Node 10): Set steps=45 (RECOMMENDED)"
echo "      • Method 2 (Node 11): Set steps=40 or steps=1 (disable)"
echo "      • Method 3 (Node 12): Set steps=35 or steps=1 (disable)"
echo "      • Method 4 (Node 13): Set steps=50 or steps=1 (disable)"
echo ""
echo "4. ▶️ Generate & Compare Results"
echo ""
echo "💡 QUICK START:"
echo "==============="
echo "• Start with only Method 1 enabled (Node 10: steps=45, others steps=1)"
echo "• Use photorealistic prompt (Node 4)"
echo "• LoRA strength = 0.65" 
echo "• Generate and evaluate"
echo ""
echo "📖 Detailed guide: docs/MASTER_WORKFLOW_GUIDE.md"
