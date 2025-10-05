# M4 Mac Optimization Guide

## MPS (Metal Performance Shaders) Configuration

### Environment Variables
```bash
# Add to ~/.zshrc for persistent settings
export PYTORCH_ENABLE_MPS_FALLBACK=1
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
```

### Memory Management
```python
# In training scripts
import torch
torch.mps.set_per_process_memory_fraction(0.75)  # Use 75% of available memory
torch.mps.empty_cache()  # Clear cache between batches
```

## Training Optimizations

### 1. Batch Size and Accumulation
```toml
# configs/lora_config.toml
[training_arguments]
batch_size = 1
gradient_accumulation_steps = 4  # Simulate batch size of 4
```

### 2. Mixed Precision
```toml
[training_arguments]
mixed_precision = "bf16"  # Better stability than fp16 on M4
```

### 3. Gradient Checkpointing
```toml
[training_arguments]
gradient_checkpointing = true
```

### 4. Attention Optimization
```toml
[additional_network_arguments]
use_pytorch_cross_attention = true  # Faster on MPS
```

## ComfyUI Performance

### 1. Preview Settings
```python
# In run_comfyui.sh
--preview-method auto  # Automatically selects best method
--highvram  # If you have 32GB+ RAM
```

### 2. Batch Processing
- Process multiple images in parallel
- Use batch_size > 1 for consistent personas

### 3. Model Loading
```python
# Keep models in unified memory
--gpu-only  # Forces all operations to GPU/MPS
```

## Video Generation Optimizations

### 1. Resolution Strategy
- Start at 512x512 for drafts
- Upscale to 768x768 for finals
- Use 1024x1024 only for stills

### 2. Frame Count
- 8-12 FPS for smooth motion
- 16-32 frames for 2-3 second clips
- Interpolate to 24 FPS in post

### 3. AnimateDiff Settings
```json
{
  "beta_schedule": "linear",
  "motion_module": "mm_sd_v15_v2.ckpt",
  "context_length": 16
}
```

## System-Level Optimizations

### 1. Virtual Memory
```bash
# Increase swap if needed
sudo sysctl vm.swapusage
```

### 2. Process Priority
```bash
# Run with high priority
nice -n -10 python train_lora.sh
```

### 3. Background Processes
- Close unnecessary apps
- Disable Time Machine during training
- Turn off Spotlight indexing

## Monitoring Performance

### 1. GPU Usage
```bash
# Monitor MPS usage
sudo powermetrics --samplers gpu_power -i1000
```

### 2. Memory Pressure
```bash
# Watch memory usage
vm_stat 1
```

### 3. Training Metrics
```python
# In training script
from torch.profiler import profile, ProfilerActivity

with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
    # Training step
    pass
print(prof.key_averages().table())
```

## Troubleshooting

### MPS Errors
```python
# Fallback to CPU for unsupported ops
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
```

### Memory Issues
```python
# Reduce memory usage
torch.backends.mps.gc_collect()
torch.mps.synchronize()
```

### Slow Training
1. Check Activity Monitor for thermal throttling
2. Use external cooling if needed
3. Reduce batch size or resolution

## Recommended Settings by RAM

### 16GB Unified Memory
- Batch size: 1
- Resolution: 768x768
- Gradient accumulation: 4
- Network dim: 32-64

### 24GB Unified Memory
- Batch size: 1-2
- Resolution: 1024x1024
- Gradient accumulation: 2-4
- Network dim: 64-128

### 32GB+ Unified Memory
- Batch size: 2-4
- Resolution: 1024x1024
- Gradient accumulation: 1-2
- Network dim: 128-256

## Quick Performance Wins

1. **Use Latest PyTorch Nightly**
   ```bash
   pip install --pre torch torchvision --index-url https://download.pytorch.org/whl/nightly/cpu
   ```

2. **Optimize Images Before Training**
   - Convert to RGB
   - Resize to exact dimensions
   - Use consistent format (PNG/JPEG)

3. **Cache Latents**
   ```toml
   [dataset_arguments]
   cache_latents = true
   cache_latents_to_disk = true
   ```

4. **Disable Logging During Training**
   ```toml
   [training_arguments]
   log_with = "none"  # Only for production runs
   ```
