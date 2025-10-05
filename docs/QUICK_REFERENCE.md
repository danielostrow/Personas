# Persona Generation - Quick Reference

## Essential Commands

### 1. Create Persona
```bash
python scripts/persona_manager.py add --name "John Doe"
```
Creates: `persona-john_doe`

### 2. List Personas
```bash
python scripts/persona_manager.py list
```

### 3. Prepare Training Data
```bash
# Add images to: training_data/persona-john_doe/raw/
python scripts/prepare_training_data.py --persona-id persona-john_doe
```

### 4. Train
```bash
./scripts/train_lora.sh persona-john_doe
```

### 5. Create Workflow
```bash
python persona_gen.py create-workflow --persona-id persona-john_doe
```

### 6. Start ComfyUI
```bash
./scripts/run_comfyui.sh
```
Open: http://localhost:8188

## Prompt Examples

### Single Persona
```
"professional photo of persona-john_doe, business suit, studio lighting"
```

### Multiple Personas
```
"persona-john_doe and persona-jane_smith shaking hands, office setting"
```

## Directory Structure
- **Training Images**: `training_data/persona-NAME/raw/`
- **Trained LoRAs**: `models/loras/`
- **Workflows**: `workflows/`
- **Generated Images**: `outputs/images/`

## Tips
- Always use exact trigger word: `persona-name`
- 20-30 training images minimum
- Training takes ~30-45 minutes
- LoRA strength: 0.7-0.9
- Multiple personas: reduce strength to 0.6-0.7

## Troubleshooting
- **Not appearing**: Check trigger word spelling
- **Wrong person**: Train more steps (6000-8000)
- **Blending**: Reduce LoRA strengths
- **Low quality**: Add "masterpiece, highly detailed, 8k"
