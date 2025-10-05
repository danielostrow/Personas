# Multi-Persona Generation Guide

This guide explains how to create and use multiple personas in your image generation workflow.

## Persona Naming Convention

All personas follow the format: `persona-<name>`
- Example: `persona-alice`, `persona-bob_smith`, `persona-john_doe`

## Step-by-Step Guide

### 1. Create Multiple Personas

```bash
# Create first persona
python scripts/persona_manager.py add --name "Alice Smith" --description "Professional woman, 30s"

# Create second persona  
python scripts/persona_manager.py add --name "Bob Johnson" --description "Business man, 40s"

# Create with custom trigger word
python scripts/persona_manager.py add --name "Charlie Lee" --trigger-word "persona-charlie"
```

### 2. Organize Training Data

Each persona has its own directory:
```
training_data/
├── persona-alice_smith/
│   └── raw/
│       ├── alice_001.jpg
│       ├── alice_002.jpg
│       └── ... (20-30 images)
├── persona-bob_johnson/
│   └── raw/
│       ├── bob_001.jpg
│       └── ...
```

### 3. Train Each Persona

```bash
# Process and train Alice
python scripts/prepare_training_data.py --persona-id persona-alice_smith
./scripts/train_lora.sh persona-alice_smith

# Process and train Bob
python scripts/prepare_training_data.py --persona-id persona-bob_johnson
./scripts/train_lora.sh persona-bob_johnson
```

### 4. Generate Multi-Persona Workflows

```bash
# Generate workflow for two personas
python scripts/persona_manager.py generate-workflow \
  persona-alice_smith persona-bob_johnson \
  --prompt "professional meeting" \
  --output workflows/alice_bob_meeting.json
```

### 5. Use in ComfyUI

Load the generated workflow in ComfyUI and use prompts like:

#### Single Persona
```
"professional photo of persona-alice_smith, business attire, office background"
```

#### Two Personas Together
```
"persona-alice_smith and persona-bob_johnson having a meeting, conference room, 
professional lighting, both in business suits"
```

#### Multiple Personas with Positioning
```
"group photo, persona-alice_smith on the left wearing blue, 
persona-bob_johnson in the center wearing gray suit, 
persona-charlie_lee on the right wearing black, 
office lobby background, professional photography"
```

## Advanced Usage

### Mixing Strengths

When using multiple personas, the workflow automatically reduces LoRA strength to 0.7 for each to prevent conflicts. You can adjust this in the workflow JSON.

### Persona Interactions

For better results when showing multiple personas interacting:

1. **Use clear positioning**: "on the left", "in the center", "sitting", "standing"
2. **Describe clothing**: Helps differentiate personas
3. **Specify actions**: "shaking hands", "having conversation", "presenting"

### Example Prompts

#### Business Meeting
```
"cinematic photo, conference room, persona-alice_smith presenting at whiteboard,
persona-bob_johnson and persona-charlie_lee seated at table taking notes,
professional lighting, depth of field"
```

#### Casual Scene
```
"candid photo, coffee shop, persona-alice_smith and persona-bob_johnson 
chatting over coffee, warm lighting, bokeh background, relaxed atmosphere"
```

#### Group Portrait
```
"professional group portrait, persona-alice_smith, persona-bob_johnson, 
and persona-charlie_lee standing together, studio lighting, neutral background,
formal business attire, smiling"
```

## Tips for Best Results

1. **Train with Variety**: Include diverse angles, expressions, and lighting in training data
2. **Use Unique Names**: Avoid similar persona names to prevent confusion
3. **Test Individually First**: Ensure each persona works well alone before combining
4. **Adjust Strengths**: If personas blend too much, reduce LoRA strengths
5. **Clear Descriptions**: Be specific about who should appear where

## Troubleshooting

### Personas Blending Together
- Reduce LoRA strengths in the workflow
- Use more distinctive trigger words
- Add more specific descriptions (clothing, position)

### Missing Persona
- Ensure the persona is properly trained
- Check that the trigger word is spelled correctly
- Verify the LoRA file exists in models/loras/

### Quality Issues
- Train with more steps (6000-8000)
- Use higher quality training images
- Ensure training images are properly cropped and centered
