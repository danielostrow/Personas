#!/bin/bash
set -e

# Enhanced Persona Quality Improvement Script
PERSONA_ID="${1:-}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ -z "$PERSONA_ID" ]; then
    echo "❌ Usage: $0 <persona-id>"
    echo "   Example: $0 persona-saramillie"
    exit 1
fi

echo "🚀 Starting Enhanced Persona Quality Improvement for: $PERSONA_ID"
echo "=================================================="

# Step 1: Enhance training captions with feature focus
echo "📝 Step 1: Enhancing training captions with feature focus..."
cd "$PROJECT_ROOT"
source venv/bin/activate
python scripts/enhance_training_captions.py --persona-id "$PERSONA_ID" --focus-features
echo "✅ Feature-focused captions generated"

# Step 2: Retrain with enhanced captions
echo "🔄 Step 2: Retraining LoRA with enhanced captions..."
./scripts/train_lora.sh "$PERSONA_ID" 1e-4 8000
echo "✅ LoRA retrained with enhanced captions"

# Step 3: Create feature validation workflow
echo "🎯 Step 3: Creating feature validation workflow..."
python scripts/create_feature_validation_workflow.py --persona-id "$PERSONA_ID"
echo "✅ Feature validation workflow created"

# Step 4: Sync to ComfyUI
echo "🔄 Step 4: Syncing models and workflows to ComfyUI..."
./scripts/sync_workflows.sh
echo "✅ Models and workflows synced"

# Step 5: Restart ComfyUI to clear cache
echo "♻️  Step 5: Restarting ComfyUI to clear cache..."
./scripts/restart_comfyui.sh
echo "✅ ComfyUI restarted"

echo ""
echo "🎉 ENHANCED PERSONA QUALITY SETUP COMPLETE!"
echo "=================================================="
echo ""
echo "🎯 Next Steps:"
echo "1. Load workflow: ${PERSONA_ID}_FEATURE_VALIDATION"
echo "2. Run the workflow to generate 6 test images"
echo "3. Compare results:"
echo "   • Eyes Focus (0.6 LoRA): Check eye accuracy"
echo "   • Facial Features (0.75 LoRA): Check face structure"  
echo "   • Ultra Realistic (0.9 LoRA): Check overall likeness"
echo "4. Use upscaled versions to inspect fine details"
echo "5. Select the best LoRA strength for final work"
echo ""
echo "💡 Quality Tips:"
echo "• Look for accurate eye color and shape"
echo "• Check facial structure matches training photos"
echo "• Verify skin tone and texture realism"
echo "• Ensure natural expressions without AI artifacts"
echo ""
echo "🔧 If still not satisfied:"
echo "• Add more diverse training photos (different angles/lighting)"
echo "• Focus on close-up face shots in training data"
echo "• Run: python scripts/enhance_training_captions.py --persona-id $PERSONA_ID --focus-features"
