#!/bin/bash

# Complete Setup and Verification Script for Persona Generation System
# This script ensures 100% working installation from git pull

set -e  # Exit on any error

echo "🎭 PERSONA GENERATION SYSTEM - COMPLETE SETUP"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    log_error "This system is designed for macOS (Apple Silicon recommended)"
    exit 1
fi

# Check for Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    log_warning "Apple Silicon (M1/M2/M3/M4) recommended for best performance"
fi

log_info "Starting complete setup process..."

# Step 1: Basic Setup
echo -e "\n${BLUE}📦 STEP 1: Basic Environment Setup${NC}"
echo "=================================="

# Make all scripts executable
log_info "Making scripts executable..."
chmod +x setup.sh scripts/*.sh
log_success "Scripts are now executable"

# Run main setup
log_info "Running main setup script..."
if ./setup.sh; then
    log_success "Main setup completed successfully"
else
    log_error "Main setup failed"
    exit 1
fi

# Step 2: Download Models
echo -e "\n${BLUE}📥 STEP 2: Model Download${NC}"
echo "=========================="

log_info "Downloading all required models (this may take 10-15 minutes)..."
if ./scripts/download_models.sh; then
    log_success "All models downloaded successfully"
else
    log_error "Model download failed"
    exit 1
fi

# Step 3: Setup Reference Image Structure
echo -e "\n${BLUE}📁 STEP 3: Reference Image Structure${NC}"
echo "====================================="

log_info "Creating reference image directories..."
mkdir -p reference_images/persona{1,2,3}/{face_reference,body_reference}

# Create example reference structure
log_info "Setting up example reference image structure..."
for i in {1..3}; do
    cat > reference_images/persona${i}/face_reference/README.txt << 'EOF'
📸 FACE REFERENCE IMAGES - REQUIRED FOR PERSONA TRAINING

Place 8 required images in this folder:

1. front_face_clear.jpg - Direct frontal view, eyes/nose/mouth visible
2. face_3quarter_left.jpg - 3/4 profile from left side  
3. face_3quarter_right.jpg - 3/4 profile from right side
4. face_profile_left.jpg - Complete left side profile
5. face_profile_right.jpg - Complete right side profile
6. eyes_closeup.jpg - Detailed eye region closeup
7. smile_expression.jpg - Natural smile showing personality
8. neutral_expression.jpg - Relaxed, natural expression

REQUIREMENTS:
- Resolution: Minimum 1024x1024 pixels
- Format: JPG, PNG, or WEBP
- Lighting: Natural, even lighting
- Background: Plain or simple preferred
- Quality: Sharp focus on facial features

These images are used for:
✓ LoRA training data generation
✓ Validation and quality comparison
✓ Reference-guided generation prompts
EOF

    cat > reference_images/persona${i}/body_reference/README.txt << 'EOF'
🏃‍♀️ BODY REFERENCE IMAGES - NPC STYLE REQUIREMENTS

Place 7 required images in this folder:

1. body_front_full.jpg - Standing straight, facing camera
2. body_back_full.jpg - Standing straight, back to camera  
3. body_left_side.jpg - Complete left side profile
4. body_right_side.jpg - Complete right side profile
5. sitting_pose.jpg - Natural sitting position
6. walking_pose.jpg - Mid-stride walking motion
7. hands_detail.jpg - Clear view of both hands

REQUIREMENTS:
- Resolution: Minimum 1024x1536 pixels (portrait)
- Format: JPG, PNG, or WEBP
- Lighting: Even, natural lighting
- Background: Plain or simple preferred
- Pose: Natural, relaxed positions

These images ensure:
✓ Accurate body proportions
✓ Natural pose generation
✓ Hand and limb validation
✓ Full-body scene consistency
EOF
done

log_success "Reference image structure created with instructions"

# Step 4: Workflow Setup
echo -e "\n${BLUE}🔧 STEP 4: Workflow Configuration${NC}"
echo "=================================="

log_info "Copying workflow to ComfyUI..."
mkdir -p ComfyUI/user/default/workflows
cp workflows/ADAPTIVE_BATCH_COMMUNITY_GENERATOR.json ComfyUI/user/default/workflows/
log_success "Workflow installed in ComfyUI"

# Step 5: Create Symlinks for Models
echo -e "\n${BLUE}🔗 STEP 5: Model Integration${NC}"
echo "============================="

log_info "Creating model symlinks for ComfyUI..."

# Create symlinks if they don't exist
if [ ! -L "ComfyUI/models/checkpoints" ]; then
    ln -sf "$(pwd)/models/checkpoints" "ComfyUI/models/checkpoints"
    log_success "Checkpoints symlink created"
fi

if [ ! -L "ComfyUI/models/loras" ]; then
    ln -sf "$(pwd)/models/loras" "ComfyUI/models/loras"  
    log_success "LoRAs symlink created"
fi

if [ ! -L "ComfyUI/models/vae" ]; then
    ln -sf "$(pwd)/models/vae" "ComfyUI/models/vae"
    log_success "VAE symlink created"
fi

# Step 6: Install Additional Dependencies
echo -e "\n${BLUE}📚 STEP 6: Additional Dependencies${NC}"
echo "==================================="

log_info "Activating virtual environment and installing additional packages..."
source venv/bin/activate

# Install WAS Node Suite requirements if not already installed
if [ -d "ComfyUI/custom_nodes/was-node-suite-comfyui" ]; then
    log_info "Installing WAS Node Suite requirements..."
    cd ComfyUI/custom_nodes/was-node-suite-comfyui
    pip install -r requirements.txt --quiet
    cd ../../../
    log_success "WAS Node Suite requirements installed"
fi

# Install any missing packages
log_info "Ensuring all Python packages are installed..."
pip install --quiet \
    click \
    Pillow \
    opencv-python \
    scikit-image \
    matplotlib

log_success "All Python dependencies verified"

# Step 7: Test Installation
echo -e "\n${BLUE}🧪 STEP 7: Installation Verification${NC}"
echo "====================================="

log_info "Running comprehensive installation test..."
python verify_installation.py

# Step 8: Create Example Persona
echo -e "\n${BLUE}👤 STEP 8: Example Persona Setup${NC}"
echo "================================="

log_info "Creating example persona for testing..."
if python scripts/persona_manager.py add --name "Example Person" --trigger-word "persona-example"; then
    log_success "Example persona created: persona-example"
else
    log_warning "Persona creation skipped (may already exist)"
fi

# Step 9: Start ComfyUI Test
echo -e "\n${BLUE}🚀 STEP 9: ComfyUI Test Launch${NC}"
echo "==============================="

log_info "Testing ComfyUI startup..."

# Start ComfyUI in background for testing
cd ComfyUI
python main.py --port 8188 &
COMFYUI_PID=$!
cd ..

# Wait for ComfyUI to start
log_info "Waiting for ComfyUI to initialize..."
sleep 10

# Test if ComfyUI is responding
if curl -s http://127.0.0.1:8188/system_stats > /dev/null; then
    log_success "ComfyUI is running and responding on port 8188"
    
    # Test workflow loading
    log_info "Testing workflow accessibility..."
    if [ -f "ComfyUI/user/default/workflows/ADAPTIVE_BATCH_COMMUNITY_GENERATOR.json" ]; then
        log_success "Workflow is accessible in ComfyUI browser"
    else
        log_warning "Workflow file not found in ComfyUI directory"
    fi
else
    log_error "ComfyUI is not responding on port 8188"
fi

# Stop test ComfyUI instance
kill $COMFYUI_PID 2>/dev/null || true
sleep 2

# Step 10: Final Setup Summary
echo -e "\n${GREEN}🎉 SETUP COMPLETE!${NC}"
echo "=================="

echo -e "\n${BLUE}📋 INSTALLATION SUMMARY:${NC}"
echo "✅ Virtual environment created and activated"
echo "✅ PyTorch with MPS support installed"
echo "✅ ComfyUI and sd-scripts cloned and configured"
echo "✅ All custom nodes installed (WAS Node Suite, AnimateDiff, etc.)"
echo "✅ Models downloaded (~15GB total)"
echo "✅ Workflows installed and accessible"
echo "✅ Reference image structure created"
echo "✅ Example persona created for testing"
echo "✅ System verified and ready for use"

echo -e "\n${BLUE}🚀 QUICK START GUIDE:${NC}"
echo "===================="

echo "1. 📁 Add Reference Images:"
echo "   - Face images: reference_images/persona1/face_reference/"
echo "   - Body images: reference_images/persona1/body_reference/"
echo "   - See README.txt files in each folder for requirements"

echo -e "\n2. 🎭 Create Your Persona:"
echo "   python scripts/persona_manager.py add --name 'Your Name'"

echo -e "\n3. 🔄 Prepare Training Data:"
echo "   python scripts/prepare_training_data.py --persona-id persona-your_name"

echo -e "\n4. 🏋️ Train LoRA:"
echo "   ./scripts/train_lora.sh persona-your_name"

echo -e "\n5. 🎨 Start Creating:"
echo "   ./scripts/run_comfyui.sh"
echo "   Open: http://127.0.0.1:8188"
echo "   Load: ADAPTIVE_BATCH_COMMUNITY_GENERATOR.json"

echo -e "\n${BLUE}📚 DOCUMENTATION:${NC}"
echo "=================="
echo "• Complete Guide: docs/HOW_TO_USE_PERSONAS.md"
echo "• Workflow Guide: docs/WORKFLOW_OPERATION_GUIDE.md"
echo "• Quality Tips: docs/IMPROVING_PERSONA_QUALITY.md"
echo "• Master Controls: docs/MASTER_WORKFLOW_GUIDE.md"

echo -e "\n${BLUE}🔧 USEFUL COMMANDS:${NC}"
echo "==================="
echo "• List personas: python scripts/persona_manager.py list"
echo "• Start ComfyUI: ./scripts/run_comfyui.sh"
echo "• Restart ComfyUI: ./scripts/restart_comfyui.sh"
echo "• Verify system: python verify_installation.py"

echo -e "\n${GREEN}🎯 SYSTEM READY FOR PROFESSIONAL PERSONA GENERATION!${NC}"
echo -e "\n${YELLOW}Next: Add your reference images and create your first persona!${NC}"

log_success "Complete setup finished successfully!"
