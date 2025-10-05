# Persona Generation System

🎭 **persona generation system** for M4 Mac with ComfyUI, LoRA training, and comprehensive validation. Create realistic digital personas with unique trigger words that can be combined in scenes.

## 🚀 Complete Installation Guide (From Git Pull)

### Prerequisites
- **Apple Silicon Mac** (M1/M2/M3/M4)
- **16GB+ RAM** recommended  
- **50GB+ free disk space**
- **macOS 13.0+**
- **Python 3.10+**

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone <repository-url> persona
cd persona

# Make scripts executable
chmod +x setup.sh scripts/*.sh

# Run complete automated setup (takes 10-15 minutes)
./setup.sh
```

**What `setup.sh` does:**
- Creates Python virtual environment
- Installs PyTorch with MPS support
- Clones ComfyUI and sd-scripts
- Installs all dependencies
- Sets up custom nodes (WAS Node Suite, AnimateDiff, etc.)

### Step 2: Download Models

```bash
# Download all required models (SDXL, VAE, AnimateDiff, ControlNet)
./scripts/download_models.sh
```

**Downloads (~15GB):**
- SDXL Base 1.0 + Refiner
- SDXL VAE
- AnimateDiff motion model
- ControlNet OpenPose
- RealESRGAN upscaling models

### Step 3: Start ComfyUI

```bash
# Start ComfyUI server
./scripts/run_comfyui.sh

# Or manually:
cd ComfyUI && python main.py --port 8188
```

**Access ComfyUI:** Open http://127.0.0.1:8188

### Step 4: Verify Installation

```bash
# Test system setup
python test_setup.py
```

**Expected output:**
```
✅ Virtual environment: Active
✅ PyTorch MPS: Available  
✅ ComfyUI: Installed
✅ sd-scripts: Installed
✅ Models: Downloaded
✅ WAS Node Suite: 220 nodes loaded
✅ System ready for persona generation!
```

## 🎯 Quick Start - Create Your First Persona

### Step 1: Create Persona

```bash
# Create new persona
python scripts/persona_manager.py add --name "Sarah Miller"
# Creates: persona-sarah_miller (trigger word: persona-sarah_miller)
```

### Step 2: Prepare Reference Images

**Required folder structure:**
```
reference_images/persona1/
├── face_reference/          (8 required images)
│   ├── front_face_clear.jpg    (Direct frontal, eyes/nose/mouth visible)
│   ├── face_3quarter_left.jpg  (3/4 profile, ear visible)
│   ├── face_3quarter_right.jpg (3/4 profile, ear visible)
│   ├── face_profile_left.jpg   (Full side profile)
│   ├── face_profile_right.jpg  (Full side profile)
│   ├── eyes_closeup.jpg        (Detailed eye region)
│   ├── smile_expression.jpg    (Natural smile)
│   └── neutral_expression.jpg  (Relaxed expression)
└── body_reference/          (7 required images)
    ├── body_front_full.jpg     (Front view, full body)
    ├── body_back_full.jpg      (Back view, full body)
    ├── body_left_side.jpg      (Left profile, full body)
    ├── body_right_side.jpg     (Right profile, full body)
    ├── sitting_pose.jpg        (Natural sitting)
    ├── walking_pose.jpg        (Mid-stride movement)
    └── hands_detail.jpg        (Clear hand reference)
```

**Image Requirements:**
- **Resolution:** 1024x1024+ (faces), 1024x1536+ (bodies)
- **Quality:** Sharp focus, natural lighting
- **Background:** Plain or simple preferred
- **Format:** JPG, PNG, or WEBP

### Step 3: Prepare Training Data

```bash
# Process reference images for training
python scripts/prepare_training_data.py --persona-id persona-sarah_miller
```

### Step 4: Train LoRA

```bash
# Train persona LoRA (takes 30-60 minutes)
./scripts/train_lora.sh persona-sarah_miller

# Monitor training progress
tail -f logs/persona-sarah_miller_training.log
```

### Step 5: Load Workflow in ComfyUI

1. **Open ComfyUI** (http://127.0.0.1:8188)
2. **Load Workflow:** Menu → Load → `ADAPTIVE_BATCH_COMMUNITY_GENERATOR.json`
3. **Configure LoRA:** Set `PERSONA1_LORA.safetensors` to `persona-sarah_miller.safetensors`
4. **Update Prompts:** Replace `PERSONA1_TRIGGER` with `persona-sarah_miller`
5. **Queue Prompt** to generate!

## 🎛️ Master Workflow Features

The `ADAPTIVE_BATCH_COMMUNITY_GENERATOR.json` workflow includes:

### **Multi-Persona Support**
- **3 persona slots** with individual LoRA loaders
- **Adaptive generation** based on active personas
- **Batch reference image loading** (20-30 images per persona)

### **Comprehensive Validation System**
- **Face cropping + 4x upscaling** for detailed inspection
- **Edge detection analysis** for anatomical consistency  
- **AI-powered image analysis** for quality assessment
- **Reference comparison** against training images

### **Realism Enhancement**
- **3 additional LoRAs:**
  - `realistic_skin_texture.safetensors` (0.6 strength)
  - `detail_enhancer.safetensors` (0.4 strength)  
  - `photorealism_helper.safetensors` (0.5 strength)

### **Multiple Generation Modes**
- **Single Portrait:** Individual character headshots
- **Duo Portrait:** Two characters interacting
- **Group Photo:** All three characters together
- **Conversation Scene:** Natural dialogue poses
- **Outdoor Scene:** Environmental interactions
- **Video Generation:** AnimateDiff motion sequences

### **Quality Control Outputs**
- **Original Images:** `ADAPTIVE_[SCENE_TYPE]`
- **Validation Crops:** `VALIDATION_[SCENE]_FACE_4X`
- **Edge Analysis:** `EDGE_ANALYSIS_[SCENE]`
- **Upscaled Versions:** `ADAPTIVE_[SCENE]_4X`

## 📊 Workflow Operation Guide

### Loading the Workflow

1. **Start ComfyUI:** `./scripts/run_comfyui.sh`
2. **Access Interface:** http://127.0.0.1:8188
3. **Load Workflow:** Menu → Load → `ADAPTIVE_BATCH_COMMUNITY_GENERATOR.json`

### Configuring Personas

**For Single Persona:**
1. Load reference images in `reference_images/persona1/`
2. Set `PERSONA1_LORA.safetensors` to your trained LoRA
3. Update prompts with your trigger word
4. Set other persona LoRA strengths to 0

**For Multiple Personas:**
1. Load reference images in `persona1/`, `persona2/`, `persona3/` folders
2. Configure each LoRA loader with respective `.safetensors` files
3. Update all prompts with appropriate trigger words
4. Adjust LoRA strengths (0.6-0.8 range for multi-persona)

### Generation Process

1. **Queue Prompt** → Workflow begins processing
2. **Monitor Progress** → Watch node execution in real-time
3. **Review Outputs** → Check generated images in ComfyUI output folder
4. **Validation Check** → Examine cropped faces and edge analysis
5. **Quality Assessment** → Compare against reference images

### Output Organization

```
ComfyUI/output/
├── ADAPTIVE_SINGLE_PORTRAIT_00001_.png
├── ADAPTIVE_DUO_PORTRAIT_00002_.png  
├── ADAPTIVE_GROUP_PHOTO_00003_.png
├── VALIDATION_SINGLE_FACE_4X_00004_.png
├── EDGE_ANALYSIS_SINGLE_00005_.png
└── [Additional outputs...]
```

## 🔧 Advanced Configuration

### Custom LoRA Training

```bash
# Create optimized training config
python scripts/create_optimized_config.py --persona-id persona-sarah_miller

# Train with custom settings
./scripts/train_lora_with_config.sh configs/persona-sarah_miller_optimized.toml
```

### Quality Optimization

```bash
# Test different LoRA strengths
python scripts/test_lora_strengths.py --persona-id persona-sarah_miller --strengths "0.6,0.7,0.8,0.9"

# Enhanced caption generation
python scripts/generate_captions.py --persona-id persona-sarah_miller --mode detailed
```

### Multiple Personas Management

```bash
# List all personas
python scripts/persona_manager.py list

# Get persona details
python scripts/persona_manager.py info persona-sarah_miller

# Create multi-persona workflow
python scripts/persona_manager.py generate-workflow persona-sarah_miller persona-john_doe \
  --prompt "two people having coffee" \
  --output workflows/sarah_and_john.json
```

## 🎨 Prompt Engineering

### Single Persona
```
masterpiece, persona-sarah_miller wearing elegant dress, professional portrait, 
natural lighting, detailed facial features, high quality photography
```

### Multiple Personas
```
cinematic photo, persona-sarah_miller on the left talking with persona-john_doe on the right,
modern office setting, natural conversation, professional lighting, bokeh background
```

### Advanced Prompting
```
ultra realistic, persona-sarah_miller and persona-john_doe, 
detailed faces, natural skin texture, perfect anatomy, 
professional photography, 85mm lens, shallow depth of field,
avoid: cartoon, anime, artificial, plastic, duplicate faces
```

## 📚 Documentation

- 📖 **[How to Use Personas](docs/HOW_TO_USE_PERSONAS.md)** - Complete usage guide
- 🎭 **[Multi-Persona Guide](docs/MULTI_PERSONA_GUIDE.md)** - Advanced multi-character techniques  
- 🎛️ **[Master Workflow Guide](docs/MASTER_WORKFLOW_GUIDE.md)** - UI controls and features
- 🔧 **[Improving Quality](docs/IMPROVING_PERSONA_QUALITY.md)** - Optimization techniques

## 🚨 Troubleshooting

### Common Issues

**Workflow won't load:**
```bash
# Restart ComfyUI to clear cache
./scripts/restart_comfyui.sh
```

**Missing nodes error:**
```bash
# Reinstall WAS Node Suite dependencies
cd ComfyUI/custom_nodes/was-node-suite-comfyui
pip install -r requirements.txt
```

**Out of memory during training:**
```bash
# Edit training config for lower memory usage
# Reduce batch_size to 1, lower resolution to 768
```

**Poor generation quality:**
- Check reference image quality (sharp, well-lit)
- Increase training steps (6000-8000)
- Adjust LoRA strength (0.7-0.9 for single, 0.6-0.7 for multi)
- Use detailed prompts with negative prompts

### Performance Optimization

**For M4 Max/Ultra:**
- Increase batch size to 2-4
- Use higher resolution training (1024x1024)
- Enable gradient accumulation

**For M4 Base:**
- Keep batch size at 1
- Use 768x768 training resolution
- Enable gradient checkpointing

## 🎯 System Requirements

**Minimum:**
- M1 Mac with 16GB RAM
- 50GB free disk space
- macOS 13.0+

**Recommended:**
- M4 Mac with 32GB+ RAM
- 100GB+ free disk space (for multiple personas)
- macOS 14.0+

**Optimal:**
- M4 Max/Ultra with 64GB+ RAM
- 200GB+ SSD space
- External GPU enclosure (optional)

## 🔄 Updates and Maintenance

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update ComfyUI
cd ComfyUI && git pull

# Update custom nodes
cd custom_nodes/was-node-suite-comfyui && git pull

# Backup personas and models
tar -czf personas_backup.tar.gz personas.json models/loras/ reference_images/
```

## 📞 Support

For issues, questions, or feature requests:
1. Check the troubleshooting section above
2. Review the documentation in `docs/`
3. Examine log files in `logs/` directory
4. Test with the validation workflow first

The system is designed to be completely self-contained and idempotent - you can run setup multiple times safely, and all components work together seamlessly for professional persona generation.