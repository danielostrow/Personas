# 🎛️ ADAPTIVE BATCH COMMUNITY GENERATOR - Complete Workflow Guide

## Overview

The `ADAPTIVE_BATCH_COMMUNITY_GENERATOR.json` workflow is a comprehensive persona generation system with:

- **Multi-persona support** (up to 3 characters)
- **Batch reference image processing** (20-30 images per persona)
- **Comprehensive validation system** (anatomical, lighting, consistency)
- **Realism enhancement LoRAs** (skin texture, detail enhancement, photorealism)
- **Multiple generation modes** (single, duo, group, video)
- **Professional quality control** (face cropping, upscaling, edge analysis)

## 🚀 Quick Start

### 1. Load Workflow in ComfyUI

1. **Start ComfyUI:** `./scripts/run_comfyui.sh`
2. **Open Browser:** http://127.0.0.1:8188
3. **Load Workflow:** Menu → Load → `ADAPTIVE_BATCH_COMMUNITY_GENERATOR.json`

### 2. Basic Configuration

**For Single Persona Generation:**
1. **Set LoRA:** Node 10 → `PERSONA1_LORA.safetensors` → your trained LoRA file
2. **Update Prompts:** Replace `PERSONA1_TRIGGER` with your trigger word (e.g., `persona-sarah_miller`)
3. **Disable Other Personas:** Set nodes 11-12 LoRA strengths to 0.0
4. **Queue Prompt**

## 📊 Workflow Architecture

### Core Processing Chain

```
Reference Images → Batch Loading → Persona LoRAs → Generation → Validation → Output
     ↓                  ↓              ↓             ↓            ↓          ↓
  Face/Body         Size Detection   Realism       Multiple     Quality    Enhanced
  References        & Counting       Enhancement   Scenarios    Checks     Results
```

### Node Groups Breakdown

| Node Range | Function | Description |
|------------|----------|-------------|
| 1-15 | **Model Loading** | SDXL base, LoRAs, realism enhancers |
| 20-27 | **Text Encoding** | Prompts for different scenarios |
| 30-31 | **Latent Generation** | Empty latents for image/video |
| 40-44 | **Image Sampling** | KSamplers for different scenarios |
| 50-54 | **VAE Decoding** | Convert latents to images |
| 60-64 | **Image Saving** | Original generation outputs |
| 100-150 | **Upscaling** | 4x enhancement for quality |
| 200-206 | **Video Generation** | AnimateDiff sequences |
| 300-312 | **Reference Loading** | Batch image processing |
| 500-554 | **Validation System** | Face analysis, edge detection |
| 700-740 | **Quality Control** | Reference comparison, notes |

## 🎭 Multi-Persona Configuration

### Persona Slot Setup

**Persona 1 (Primary):**
- **Reference Path:** `reference_images/persona1/`
- **LoRA Node:** 10 (`PERSONA1_LORA.safetensors`)
- **Trigger Word:** Update all `PERSONA1_TRIGGER` instances

**Persona 2 (Secondary):**
- **Reference Path:** `reference_images/persona2/`
- **LoRA Node:** 11 (`PERSONA2_LORA.safetensors`)
- **Trigger Word:** Update all `PERSONA2_TRIGGER` instances

**Persona 3 (Tertiary):**
- **Reference Path:** `reference_images/persona3/`
- **LoRA Node:** 12 (`PERSONA3_LORA.safetensors`)
- **Trigger Word:** Update all `PERSONA3_TRIGGER` instances

### Reference Image Structure

```
reference_images/
├── persona1/
│   ├── face_reference/     (8 facial angle images)
│   └── body_reference/     (7 body pose images)
├── persona2/
│   ├── face_reference/     (8 facial angle images)  
│   └── body_reference/     (7 body pose images)
└── persona3/
    ├── face_reference/     (8 facial angle images)
    └── body_reference/     (7 body pose images)
```

## 🎨 Generation Modes

### Image Generation Scenarios

1. **Single Portrait** (Node 20)
   - **Prompt:** Professional headshot, detailed facial features
   - **Output:** `ADAPTIVE_SINGLE_PORTRAIT`
   - **Best for:** Individual character showcase

2. **Duo Portrait** (Node 21)
   - **Prompt:** Two characters together, professional photography
   - **Output:** `ADAPTIVE_DUO_PORTRAIT`
   - **Best for:** Character interactions, relationships

3. **Group Photo** (Node 22)
   - **Prompt:** All three characters, group photography
   - **Output:** `ADAPTIVE_GROUP_PHOTO`
   - **Best for:** Community scenes, team photos

4. **Conversation Scene** (Node 23)
   - **Prompt:** Characters having coffee, intimate conversation
   - **Output:** `ADAPTIVE_CONVERSATION`
   - **Best for:** Natural dialogue scenes

5. **Outdoor Scene** (Node 24)
   - **Prompt:** Characters in park setting, lifestyle photography
   - **Output:** `ADAPTIVE_OUTDOOR_SCENE`
   - **Best for:** Environmental interactions

### Video Generation Modes

1. **Single Walking** (Node 201)
   - **Prompt:** Character walking confidently, cinematic motion
   - **Output:** `ADAPTIVE_SINGLE_WALK.webp`
   - **Duration:** 16 frames at 6fps

2. **Group Activity** (Node 202)
   - **Prompt:** Multiple personas in community picnic
   - **Output:** `ADAPTIVE_GROUP_ACTIVITY.webp`
   - **Duration:** 16 frames at 6fps

## 🔧 LoRA Configuration

### Realism Enhancement Stack

1. **Persona LoRAs** (Nodes 10-12)
   - **Strength:** 0.75 (single) / 0.6-0.7 (multi)
   - **Purpose:** Character identity and features

2. **Realistic Skin Texture** (Node 13)
   - **Strength:** 0.6
   - **Purpose:** Natural skin appearance, pore detail

3. **Detail Enhancer** (Node 14)
   - **Strength:** 0.4
   - **Purpose:** Fine feature sharpening, micro-details

4. **Photorealism Helper** (Node 15)
   - **Strength:** 0.5
   - **Purpose:** Overall photographic realism

### Strength Recommendations

| Scenario | Persona LoRA | Realism LoRAs | Notes |
|----------|--------------|---------------|-------|
| **Single Character** | 0.8-0.9 | As configured | Maximum character fidelity |
| **Duo Characters** | 0.7-0.8 | As configured | Balanced character presence |
| **Group (3+)** | 0.6-0.7 | Reduce by 0.1 | Prevent character blending |
| **Video Sequences** | 0.6-0.75 | As configured | Temporal consistency |

## 🔍 Validation System

### Face Analysis Pipeline

1. **Face Cropping** (Nodes 500-504)
   - **Function:** Isolate facial regions for detailed inspection
   - **Settings:** 1.5x crop factor, center alignment
   - **Output:** Cropped face regions

2. **4x Upscaling** (Nodes 510-515)
   - **Model:** RealESRGAN_x4plus.pth
   - **Purpose:** Reveal fine facial details
   - **Output:** High-resolution face crops

3. **AI Analysis** (Nodes 520-524)
   - **Function:** Detailed anatomical and quality assessment
   - **Checks:** Eyes, ears, facial features, lighting, consistency
   - **Output:** Analysis text reports

4. **Edge Detection** (Nodes 540-544)
   - **Method:** Canny edge detection
   - **Purpose:** Anatomical structure validation
   - **Settings:** 150/50 thresholds, canny algorithm

### Quality Control Outputs

| Output Type | Prefix | Purpose |
|-------------|--------|---------|
| **Original Images** | `ADAPTIVE_*` | Main generation results |
| **Upscaled Images** | `ADAPTIVE_*_4X` | Enhanced quality versions |
| **Face Validation** | `VALIDATION_*_FACE_4X` | Detailed facial inspection |
| **Edge Analysis** | `EDGE_ANALYSIS_*` | Anatomical structure check |

### Validation Criteria

**✅ Pass Conditions:**
- **Eyes:** Symmetrical, properly aligned, natural color
- **Ears:** Correct positioning, anatomical accuracy
- **Hands:** 5 fingers, natural poses, proper proportions
- **Lighting:** Consistent direction, natural shadows
- **Anatomy:** Realistic proportions, no impossible angles

**❌ Rejection Triggers:**
- **Anatomical errors:** Extra/missing body parts
- **Lighting issues:** Impossible shadows, conflicting sources
- **Character inconsistency:** Identity drift, blending
- **Quality issues:** Severe artifacts, distortions

## ⚙️ Advanced Configuration

### Prompt Customization

**Template Structure:**
```
[Scenario Icon] [Scene Description]: [Character Triggers] [Action/Pose], 
[Photography Style], [Technical Details], [Quality Modifiers]
```

**Example Modifications:**
```
Original: "👥 GROUP PHOTO: PERSONA1_TRIGGER, PERSONA2_TRIGGER, and PERSONA3_TRIGGER standing together"

Custom: "🎬 MOVIE SCENE: persona-sarah_miller and persona-john_doe in dramatic confrontation, 
cinematic lighting, 35mm film, shallow depth of field, professional cinematography"
```

### Sampler Settings

| Node | Sampler | Steps | CFG | Scheduler | Use Case |
|------|---------|-------|-----|-----------|----------|
| 40 | dpmpp_2m | 40 | 6.0 | karras | Standard quality |
| 41 | dpmpp_2m_sde | 45 | 5.5 | karras | Enhanced detail |
| 42 | euler | 50 | 6.5 | normal | Stable generation |
| 43 | dpmpp_2m | 40 | 6.0 | karras | Consistent results |
| 44 | dpmpp_2m_sde | 45 | 5.5 | karras | High quality |

### Resolution Settings

**Image Generation:**
- **Standard:** 1024x1024 (Node 30)
- **Optimal Balance:** Speed vs. Quality

**Video Generation:**
- **Resolution:** 768x768 (Node 31)
- **Frames:** 16 frames
- **Frame Rate:** 6fps (adjustable in VHS nodes)

## 🎯 Optimization Tips

### Performance Optimization

**For M4 Base (16GB):**
```json
{
  "batch_size": 1,
  "resolution": "1024x1024",
  "video_resolution": "768x768",
  "lora_strength": "0.7-0.8"
}
```

**For M4 Max/Ultra (32GB+):**
```json
{
  "batch_size": 1,
  "resolution": "1024x1024",
  "video_resolution": "1024x1024",
  "lora_strength": "0.8-0.9"
}
```

### Quality Optimization

1. **Reference Images:**
   - Use high-resolution source images (1024x1024+)
   - Ensure consistent lighting across reference set
   - Include variety of expressions and angles

2. **LoRA Training:**
   - Train for 6000-8000 steps for better quality
   - Use detailed captions with facial feature descriptions
   - Maintain consistent trigger word usage

3. **Generation Settings:**
   - Use higher step counts (40-50) for final outputs
   - Experiment with CFG scale (5.5-7.0) for style preference
   - Enable high-quality samplers (dpmpp_2m_sde)

### Memory Management

**If encountering memory issues:**
1. **Reduce batch size** to 1 in all nodes
2. **Lower resolution** to 768x768 or 512x512
3. **Disable video generation** (set video latent to 1 frame)
4. **Reduce LoRA count** (disable realism enhancers temporarily)

## 🚨 Troubleshooting

### Common Issues

**"Node not found" errors:**
```bash
# Restart ComfyUI to reload custom nodes
./scripts/restart_comfyui.sh
```

**Poor character likeness:**
- Increase persona LoRA strength (0.8-0.9)
- Check reference image quality
- Verify trigger word consistency
- Retrain LoRA with more steps

**Character blending in multi-persona:**
- Reduce LoRA strengths (0.6-0.7)
- Use more specific prompts
- Add negative prompts: "duplicate person, same face"

**Memory errors:**
- Reduce resolution settings
- Disable some validation nodes temporarily
- Close other applications

### Validation Failures

**Poor face validation scores:**
1. **Check reference images** - ensure high quality, clear faces
2. **Adjust LoRA strength** - find optimal balance
3. **Improve prompts** - add facial detail descriptions
4. **Retrain if necessary** - with better reference images

**Inconsistent results:**
1. **Fix random seeds** - use same seed for consistency
2. **Check model versions** - ensure same SDXL checkpoint
3. **Verify LoRA files** - confirm correct persona LoRAs loaded

## 📈 Workflow Monitoring

### Real-time Progress

**ComfyUI Interface:**
- **Node execution** highlighted in real-time
- **Progress bars** for sampling operations
- **Memory usage** displayed in system stats
- **Error messages** shown in console

**Terminal Monitoring:**
```bash
# Watch ComfyUI logs
tail -f ComfyUI/user/comfyui.log

# Monitor system resources
htop
```

### Output Organization

**Generated files appear in:**
```
ComfyUI/output/
├── ADAPTIVE_SINGLE_PORTRAIT_00001_.png
├── ADAPTIVE_DUO_PORTRAIT_00002_.png
├── VALIDATION_SINGLE_FACE_4X_00003_.png
├── EDGE_ANALYSIS_SINGLE_00004_.png
└── ADAPTIVE_SINGLE_WALK_00005_.webp
```

## 🎬 Production Workflow

### Batch Processing

1. **Setup multiple personas** with reference images
2. **Configure workflow** for all active personas
3. **Queue multiple prompts** with different scenarios
4. **Monitor validation outputs** for quality control
5. **Select best results** for final production

### Quality Control Process

1. **Generate initial batch** (5-10 images per scenario)
2. **Review validation crops** for facial accuracy
3. **Check edge analysis** for anatomical correctness
4. **Compare against references** manually
5. **Adjust settings** if needed and regenerate
6. **Upscale final selections** for production use

This workflow represents the pinnacle of automated persona generation with professional-grade validation and quality control systems built in.
