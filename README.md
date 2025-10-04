# Persona Generation System

Automated, idempotent persona generation system for M4 Mac with ComfyUI and LoRA training. Supports multiple personas with unique trigger words that can be combined in a single image.

## Quick Start

```bash
# 1. Initial setup
chmod +x setup.sh scripts/*.sh
./setup.sh

# 2. Download models
./scripts/download_models.sh

# 3. Create a new persona
python scripts/persona_manager.py add --name "John Doe"
# This creates persona-john_doe with trigger word: persona-john_doe

# 4. Add training images
# Add 20-30 images to: training_data/persona-john_doe/raw/

# 5. Prepare training data
python scripts/prepare_training_data.py --persona-id persona-john_doe

# 6. Train LoRA
./scripts/train_lora.sh persona-john_doe

# 7. Start ComfyUI
./scripts/run_comfyui.sh
```

📚 **[See the complete How to Use Personas guide](docs/HOW_TO_USE_PERSONAS.md)** for detailed instructions on using your trained personas.

## Managing Multiple Personas

```bash
# Create multiple personas
python scripts/persona_manager.py add --name "Alice Smith"
python scripts/persona_manager.py add --name "Bob Johnson" --trigger-word "persona-bob"

# List all personas
python scripts/persona_manager.py list

# Get info about a specific persona
python scripts/persona_manager.py info persona-alice_smith

# Generate workflow with multiple personas
python scripts/persona_manager.py generate-workflow persona-alice_smith persona-bob_johnson \
  --prompt "two people sitting at a cafe" \
  --output workflows/alice_and_bob.json
```

## Using Multiple Personas in Prompts

After training multiple personas, you can use them together:

```
# Single persona
"masterpiece, persona-alice_smith wearing a red dress, portrait"

# Multiple personas
"masterpiece, persona-alice_smith and persona-bob_johnson shaking hands, office setting"

# Complex scene
"cinematic photo, persona-alice_smith on the left, persona-bob_johnson on the right, 
having a conversation in a modern restaurant, bokeh background"
```

## Using the CLI

```bash
# Setup everything
python persona_gen.py setup --all

# List available models
python persona_gen.py list-models

# Create workflow for a trained persona
python persona_gen.py create-workflow --persona-id persona-alice_smith --type image

# Train a persona
python persona_gen.py train --persona-id persona-alice_smith

# Start ComfyUI
python persona_gen.py start-ui
```

## Project Structure

```
persona/
├── setup.sh                 # Main setup script
├── persona_gen.py          # CLI tool
├── personas.json           # Persona registry
├── scripts/                # Automation scripts
│   ├── download_models.sh
│   ├── train_lora.sh
│   ├── prepare_training_data.py
│   ├── persona_manager.py  # Persona management
│   └── run_comfyui.sh
├── training_data/          # Training images by persona
│   ├── persona-alice_smith/
│   │   ├── raw/           # Original images
│   │   └── processed/     # Processed for training
│   └── persona-bob_johnson/
│       ├── raw/
│       └── processed/
├── models/                 # Model storage
│   ├── checkpoints/       # SDXL models
│   ├── loras/            # Trained LoRAs
│   │   ├── persona-alice_smith.safetensors
│   │   └── persona-bob_johnson.safetensors
│   ├── controlnet/       # ControlNet models
│   └── vae/              # VAE models
├── outputs/               # Generated content
│   ├── images/
│   ├── videos/
│   └── processed/
├── workflows/             # ComfyUI workflows
│   ├── persona-alice_smith_image_workflow.json
│   └── multi_alice_bob.json
└── configs/              # Configuration files
    ├── persona-alice_smith_lora_config.toml
    └── persona-alice_smith_sample_prompts.txt
```

## Training Tips

1. **Image Requirements**:
   - 20-30 high-quality images
   - Different angles, lighting, expressions
   - Clear face visibility
   - Consistent person across all images

2. **Optimization for M4**:
   - Uses MPS acceleration automatically
   - Batch size set to 1 for memory efficiency
   - Mixed precision (bf16) enabled
   - Gradient checkpointing for memory savings

3. **Quality Settings**:
   - Default: 4000 steps, 1e-4 learning rate
   - For better quality: 6000-8000 steps
   - For faster training: 2000-3000 steps

## Workflow Examples

### Image Generation
```python
# In ComfyUI, load: workflows/your_persona_image_workflow.json
# Modify prompt: "masterpiece, your_persona, cinematic portrait, 85mm lens"
```

### Video Generation
```python
# Load: workflows/your_persona_video_workflow.json
# Prompts: "your_persona walking in Tokyo, cinematic, dynamic motion"
```

## Advanced Features

1. **Batch Processing**:
   ```bash
   # Process multiple personas
   for persona in alice bob charlie; do
     ./scripts/train_lora.sh $persona
   done
   ```

2. **Custom Training Config**:
   Edit `configs/lora_config.toml` for fine-tuning

3. **Post-Processing**:
   - Use Topaz Video AI for upscaling
   - DaVinci Resolve for editing
   - Frame interpolation with RIFE

## Documentation

- 📖 **[How to Use Personas](docs/HOW_TO_USE_PERSONAS.md)** - Complete guide from creation to generation
- 🎭 **[Multi-Persona Guide](docs/MULTI_PERSONA_GUIDE.md)** - Advanced techniques for multiple personas
- ⚡ **[M4 Optimization Guide](docs/M4_OPTIMIZATION.md)** - Performance tips for Apple Silicon
- 💡 **[Example Usage](EXAMPLE_USAGE.md)** - Real-world examples and prompts

## Troubleshooting

- **Out of Memory**: Reduce batch_size to 1, lower resolution to 768
- **Slow Training**: Enable xformers, use gradient checkpointing
- **Poor Quality**: Increase training steps, check image quality
- **ComfyUI Issues**: Check model paths, verify symlinks

## System Requirements

- Apple Silicon Mac (M1/M2/M3/M4)
- 16GB+ RAM recommended
- 50GB+ free disk space
- macOS 13.0+
- Python 3.10+
