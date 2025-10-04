# How to Use Personas - Complete Guide

This guide walks you through the entire process of creating and using personas, from start to finish.

## Table of Contents
1. [Creating a Persona](#1-creating-a-persona)
2. [Preparing Training Data](#2-preparing-training-data)
3. [Training Your Persona](#3-training-your-persona)
4. [Using Your Persona in ComfyUI](#4-using-your-persona-in-comfyui)
5. [Writing Effective Prompts](#5-writing-effective-prompts)
6. [Using Multiple Personas](#6-using-multiple-personas)
7. [Troubleshooting](#7-troubleshooting)

## 1. Creating a Persona

### Basic Creation
```bash
python scripts/persona_manager.py add --name "John Doe" --description "Professional man, 30s"
```

This creates:
- **Persona ID**: `persona-john_doe`
- **Trigger Word**: `persona-john_doe` (used in prompts)
- **Training Directory**: `training_data/persona-john_doe/`

### Custom Trigger Word
```bash
python scripts/persona_manager.py add --name "John Doe" --trigger-word "johndoe_v1"
```

### View Your Personas
```bash
# List all personas
python scripts/persona_manager.py list

# Get detailed info
python scripts/persona_manager.py info persona-john_doe
```

## 2. Preparing Training Data

### Image Requirements
- **Quantity**: 20-30 images minimum
- **Quality**: High resolution, clear face visibility
- **Variety**: Different angles, expressions, lighting
- **Consistency**: Same person in all images

### Add Images
Place your images in:
```
training_data/persona-john_doe/raw/
```

### Process Images
```bash
python scripts/prepare_training_data.py --persona-id persona-john_doe
```

This will:
- Resize images to 1024x1024
- Create caption files with trigger word
- Save processed images to `training_data/persona-john_doe/processed/`

## 3. Training Your Persona

### Start Training
```bash
./scripts/train_lora.sh persona-john_doe
```

### Training Parameters (Optional)
```bash
# Custom learning rate and steps
./scripts/train_lora.sh persona-john_doe 1e-4 6000

# Parameters: persona-id learning-rate train-steps
```

### Training Time
- Default (4000 steps): ~30-45 minutes on M4 Mac
- Extended (6000-8000 steps): ~45-70 minutes

### Monitor Progress
Training saves checkpoints every 5 epochs in:
```
outputs/persona-john_doe_lora_[timestamp]/
```

## 4. Using Your Persona in ComfyUI

### Start ComfyUI
```bash
./scripts/run_comfyui.sh
```
Open http://localhost:8188 in your browser

### Method 1: Pre-made Workflows (Recommended)

1. Generate workflow:
```bash
python persona_gen.py create-workflow --persona-id persona-john_doe --type image
```

2. In ComfyUI:
   - Click "Load" in the menu
   - Select `workflows/persona-john_doe_image_workflow.json`
   - The workflow is pre-configured with your persona

3. Edit the positive prompt to include your trigger word:
```
"professional portrait of persona-john_doe, business suit, studio lighting"
```

4. Click "Queue Prompt" to generate

### Method 2: Manual Setup

1. Load any SDXL workflow
2. Add a "LoRA Loader" node:
   - Right-click → Add Node → loaders → LoRA Loader
   - Connect between Checkpoint Loader and KSampler

3. Configure LoRA Loader:
   - Select `persona-john_doe.safetensors`
   - strength_model: 0.8
   - strength_clip: 0.8

4. Use trigger word in prompts

## 5. Writing Effective Prompts

### Basic Structure
```
"[style] photo of persona-john_doe, [description], [environment], [lighting]"
```

### Examples

#### Professional Headshot
```
"professional portrait of persona-john_doe, wearing business suit, 
corporate headshot, studio lighting, shallow depth of field, 
highly detailed, 8k resolution"
```

#### Casual Scene
```
"candid photo of persona-john_doe, wearing casual t-shirt and jeans, 
sitting in coffee shop, natural window lighting, relaxed expression, 
bokeh background"
```

#### Action Shot
```
"dynamic photo of persona-john_doe giving presentation, conference room, 
pointing at screen, business casual attire, confident expression, 
cinematic lighting"
```

#### Artistic Style
```
"oil painting style portrait of persona-john_doe, Renaissance lighting, 
formal attire, dramatic shadows, masterpiece quality"
```

### Prompt Tips
1. **Always include the trigger word** exactly as shown
2. **Be specific** about clothing, pose, expression
3. **Add quality modifiers**: "highly detailed", "8k", "professional"
4. **Specify lighting**: "studio lighting", "natural light", "golden hour"
5. **Include negative prompts**: "blurry, low quality, distorted"

## 6. Using Multiple Personas

### Generate Multi-Persona Workflow
```bash
# Assuming you've trained both personas
python scripts/persona_manager.py generate-workflow \
  persona-john_doe persona-jane_smith \
  --prompt "business meeting" \
  --output workflows/john_jane_meeting.json
```

### Multi-Persona Prompts

#### Two People Interacting
```
"professional photo of persona-john_doe and persona-jane_smith 
shaking hands, modern office setting, business attire, natural lighting"
```

#### Group Photo
```
"group portrait, persona-john_doe on left wearing navy suit, 
persona-jane_smith on right wearing red dress, corporate lobby background, 
professional photography"
```

#### Complex Scene
```
"cinematic shot, persona-john_doe presenting to persona-jane_smith, 
conference room, projection screen showing charts, dynamic composition, 
professional lighting"
```

## 7. Troubleshooting

### Persona Not Appearing
- **Check trigger word spelling** - must be exact
- **Verify training completed** - check `models/loras/` for the file
- **Increase LoRA strength** - try 0.9 or 1.0
- **Use simpler prompts** - start with just the trigger word

### Wrong Person Appearing
- **More training needed** - train for 6000-8000 steps
- **Better training data** - ensure all images are the same person
- **Reduce other descriptors** - let the LoRA define appearance

### Multiple Personas Blending
- **Reduce LoRA strengths** - use 0.6-0.7 for each
- **Use positioning** - "on the left", "on the right"
- **Add distinguishing features** - clothing colors, accessories

### Poor Quality Results
- **Add quality tags**: "masterpiece", "best quality", "highly detailed"
- **Specify resolution**: "8k", "4k photography"
- **Check negative prompt**: Include "low quality, blurry, distorted"
- **Adjust CFG scale**: Try 7-9 for better adherence

## Quick Command Reference

```bash
# Create persona
python scripts/persona_manager.py add --name "Name Here"

# List personas
python scripts/persona_manager.py list

# Prepare data
python scripts/prepare_training_data.py --persona-id persona-name_here

# Train
./scripts/train_lora.sh persona-name_here

# Create workflow
python persona_gen.py create-workflow --persona-id persona-name_here

# Start ComfyUI
./scripts/run_comfyui.sh
```

## Next Steps

- Read [Multi-Persona Guide](MULTI_PERSONA_GUIDE.md) for advanced techniques
- Check [M4 Optimization Guide](M4_OPTIMIZATION.md) for performance tips
- See [Example Usage](../EXAMPLE_USAGE.md) for real-world scenarios
