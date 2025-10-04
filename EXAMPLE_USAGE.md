# Example: Creating Two Personas

This example shows how to create and use two personas together.

## 1. Create Personas

```bash
# Create Alice
python scripts/persona_manager.py add --name "Alice Chen" \
  --description "Professional woman, Asian, 28 years old"

# Create Bob  
python scripts/persona_manager.py add --name "Bob Smith" \
  --description "Business executive, Caucasian, 35 years old"
```

This creates:
- `persona-alice_chen` with trigger word `persona-alice_chen`
- `persona-bob_smith` with trigger word `persona-bob_smith`

## 2. Add Training Images

Place 20-30 high-quality images in:
- `training_data/persona-alice_chen/raw/`
- `training_data/persona-bob_smith/raw/`

## 3. Process and Train

```bash
# Process Alice's images
python scripts/prepare_training_data.py --persona-id persona-alice_chen

# Train Alice
./scripts/train_lora.sh persona-alice_chen

# Process Bob's images  
python scripts/prepare_training_data.py --persona-id persona-bob_smith

# Train Bob
./scripts/train_lora.sh persona-bob_smith
```

## 4. Generate Images

### Single Persona

```bash
# Create workflow for Alice
python persona_gen.py create-workflow --persona-id persona-alice_chen --type image

# Start ComfyUI
./scripts/run_comfyui.sh

# Load the workflow and use prompts like:
"professional headshot of persona-alice_chen, business attire, studio lighting"
```

### Multiple Personas Together

```bash
# Generate multi-persona workflow
python scripts/persona_manager.py generate-workflow \
  persona-alice_chen persona-bob_smith \
  --prompt "business meeting" \
  --output workflows/alice_bob_meeting.json

# Load in ComfyUI and use prompts like:
"persona-alice_chen and persona-bob_smith shaking hands in modern office, 
professional attire, natural lighting, depth of field"
```

## 5. Example Prompts

### Professional Meeting
```
"cinematic photo, persona-alice_chen presenting to persona-bob_smith, 
conference room, projector screen in background, business formal attire, 
professional lighting, 8k, ultra detailed"
```

### Casual Interaction
```
"candid photo, persona-alice_chen and persona-bob_smith having coffee, 
casual business attire, modern cafe, warm lighting, bokeh background"
```

### Group Photo
```
"professional group photo, persona-alice_chen on left wearing navy suit,
persona-bob_smith on right wearing gray suit, corporate lobby background,
both smiling, studio lighting"
```

## Tips

1. **Consistent Training**: Use similar lighting and quality for all training images
2. **Unique Features**: Include diverse angles and expressions in training data  
3. **Clear Descriptions**: Be specific about positioning and clothing
4. **Test Individually**: Verify each persona works alone before combining
5. **Adjust Strengths**: Lower LoRA strengths (0.6-0.7) when using multiple personas
