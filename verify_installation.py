#!/usr/bin/env python3
"""
Installation Verification Script for Persona Generation System
Checks all components and provides detailed status report
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_section(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)

def check_item(item, status, details=""):
    status_icon = "✅" if status else "❌"
    print(f"{status_icon} {item}")
    if details:
        print(f"   {details}")
    return status

def run_command(cmd, capture_output=True):
    """Run command and return success status and output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def check_file_exists(path, description=""):
    """Check if file exists and return status with size info"""
    if os.path.exists(path):
        size = os.path.getsize(path)
        size_mb = size / (1024 * 1024)
        details = f"({size_mb:.1f} MB)" if size_mb > 1 else f"({size} bytes)"
        return True, details
    return False, "Not found"

def main():
    print("🎭 PERSONA GENERATION SYSTEM - INSTALLATION VERIFICATION")
    print("=" * 70)
    
    all_good = True
    
    # Check Python Environment
    check_section("PYTHON ENVIRONMENT")
    
    # Virtual environment
    venv_active = os.environ.get('VIRTUAL_ENV') is not None
    if venv_active:
        venv_path = os.environ['VIRTUAL_ENV']
        all_good &= check_item("Virtual Environment", True, f"Active: {venv_path}")
    else:
        all_good &= check_item("Virtual Environment", False, "Not activated - run 'source venv/bin/activate'")
    
    # Python version
    python_version = sys.version.split()[0]
    python_ok = tuple(map(int, python_version.split('.')[:2])) >= (3, 10)
    all_good &= check_item("Python Version", python_ok, f"Version: {python_version}")
    
    # PyTorch MPS
    try:
        import torch
        mps_available = torch.backends.mps.is_available()
        all_good &= check_item("PyTorch MPS", mps_available, f"PyTorch: {torch.__version__}")
    except ImportError:
        all_good &= check_item("PyTorch", False, "Not installed")
    
    # Check Core Dependencies
    check_section("CORE DEPENDENCIES")
    
    core_packages = [
        ('transformers', 'Transformers'),
        ('accelerate', 'Accelerate'), 
        ('diffusers', 'Diffusers'),
        ('PIL', 'Pillow'),
        ('cv2', 'OpenCV'),
        ('click', 'Click CLI')
    ]
    
    for package, name in core_packages:
        try:
            __import__(package)
            all_good &= check_item(f"{name}", True, "Installed")
        except ImportError:
            all_good &= check_item(f"{name}", False, "Missing - run pip install")
    
    # Check Project Structure
    check_section("PROJECT STRUCTURE")
    
    required_dirs = [
        ('ComfyUI', 'ComfyUI Installation'),
        ('sd-scripts', 'SD-Scripts Installation'),
        ('models', 'Models Directory'),
        ('scripts', 'Scripts Directory'),
        ('workflows', 'Workflows Directory'),
        ('reference_images', 'Reference Images Directory'),
        ('docs', 'Documentation Directory')
    ]
    
    for dir_name, description in required_dirs:
        exists = os.path.isdir(dir_name)
        all_good &= check_item(description, exists, f"Path: {dir_name}")
    
    # Check ComfyUI Custom Nodes
    check_section("COMFYUI CUSTOM NODES")
    
    custom_nodes = [
        ('ComfyUI/custom_nodes/was-node-suite-comfyui', 'WAS Node Suite'),
        ('ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved', 'AnimateDiff'),
        ('ComfyUI/custom_nodes/ComfyUI-VideoHelperSuite', 'Video Helper Suite'),
        ('ComfyUI/custom_nodes/ComfyUI_essentials', 'ComfyUI Essentials'),
        ('ComfyUI/custom_nodes/comfyui_controlnet_aux', 'ControlNet Aux')
    ]
    
    for path, name in custom_nodes:
        exists = os.path.isdir(path)
        all_good &= check_item(name, exists, f"Path: {path}")
    
    # Check Models
    check_section("DOWNLOADED MODELS")
    
    models_to_check = [
        ('models/checkpoints/sd_xl_base_1.0.safetensors', 'SDXL Base Model'),
        ('models/checkpoints/sd_xl_refiner_1.0.safetensors', 'SDXL Refiner'),
        ('models/vae/sdxl_vae.safetensors', 'SDXL VAE'),
        ('ComfyUI/models/animatediff_models/mm_sd_v15_v2.ckpt', 'AnimateDiff Model'),
        ('ComfyUI/models/controlnet/control_v11p_sd15_openpose.pth', 'ControlNet OpenPose'),
        ('ComfyUI/models/upscale_models/RealESRGAN_x4plus.pth', 'RealESRGAN 4x'),
        ('ComfyUI/models/upscale_models/RealESRGAN_x2plus.pth', 'RealESRGAN 2x')
    ]
    
    total_size = 0
    for model_path, name in models_to_check:
        exists, details = check_file_exists(model_path)
        all_good &= check_item(name, exists, details)
        if exists:
            size_mb = os.path.getsize(model_path) / (1024 * 1024)
            total_size += size_mb
    
    print(f"\n📊 Total Model Size: {total_size:.1f} MB ({total_size/1024:.1f} GB)")
    
    # Check Scripts
    check_section("EXECUTABLE SCRIPTS")
    
    scripts_to_check = [
        ('setup.sh', 'Main Setup Script'),
        ('scripts/download_models.sh', 'Model Download Script'),
        ('scripts/train_lora.sh', 'LoRA Training Script'),
        ('scripts/run_comfyui.sh', 'ComfyUI Launch Script'),
        ('scripts/restart_comfyui.sh', 'ComfyUI Restart Script')
    ]
    
    for script_path, name in scripts_to_check:
        exists = os.path.isfile(script_path)
        if exists:
            executable = os.access(script_path, os.X_OK)
            status = executable
            details = "Executable" if executable else "Not executable - run chmod +x"
        else:
            status = False
            details = "File not found"
        all_good &= check_item(name, status, details)
    
    # Check Workflows
    check_section("WORKFLOW FILES")
    
    workflow_files = [
        ('workflows/ADAPTIVE_BATCH_COMMUNITY_GENERATOR.json', 'Master Community Workflow')
    ]
    
    for workflow_path, name in workflow_files:
        exists, details = check_file_exists(workflow_path)
        if exists:
            # Validate JSON
            try:
                with open(workflow_path, 'r') as f:
                    workflow_data = json.load(f)
                node_count = len(workflow_data.get('nodes', []))
                details += f" - {node_count} nodes"
            except json.JSONDecodeError:
                details += " - Invalid JSON"
                exists = False
        all_good &= check_item(name, exists, details)
    
    # Check ComfyUI Integration
    check_section("COMFYUI INTEGRATION")
    
    comfyui_files = [
        ('ComfyUI/user/default/workflows/ADAPTIVE_BATCH_COMMUNITY_GENERATOR.json', 'Workflow in ComfyUI'),
        ('ComfyUI/models/checkpoints', 'ComfyUI Checkpoints Symlink'),
        ('ComfyUI/models/loras', 'ComfyUI LoRAs Symlink'),
        ('ComfyUI/models/vae', 'ComfyUI VAE Symlink')
    ]
    
    for path, name in comfyui_files:
        exists = os.path.exists(path)
        if exists and os.path.islink(path):
            details = f"Symlink → {os.readlink(path)}"
        elif exists:
            details = "Direct path"
        else:
            details = "Missing"
        all_good &= check_item(name, exists, details)
    
    # Check Documentation
    check_section("DOCUMENTATION")
    
    doc_files = [
        ('docs/HOW_TO_USE_PERSONAS.md', 'Usage Guide'),
        ('docs/MASTER_WORKFLOW_GUIDE.md', 'Workflow Guide'),
        ('docs/IMPROVING_PERSONA_QUALITY.md', 'Quality Guide'),
        ('reference_images/persona1/face_reference/README.txt', 'Face Reference Guide'),
        ('reference_images/persona1/body_reference/README.txt', 'Body Reference Guide')
    ]
    
    for doc_path, name in doc_files:
        exists, details = check_file_exists(doc_path)
        all_good &= check_item(name, exists, details)
    
    # Test ComfyUI Connection
    check_section("COMFYUI SERVER TEST")
    
    # Check if ComfyUI is running
    success, output = run_command("curl -s http://127.0.0.1:8188/system_stats")
    if success:
        all_good &= check_item("ComfyUI Server", True, "Running on port 8188")
    else:
        all_good &= check_item("ComfyUI Server", False, "Not running - start with ./scripts/run_comfyui.sh")
    
    # Final Status
    check_section("INSTALLATION STATUS")
    
    if all_good:
        print("🎉 INSTALLATION COMPLETE!")
        print("✅ All components verified and ready")
        print("\n🚀 Next Steps:")
        print("1. Create your first persona: python scripts/persona_manager.py add --name 'Your Name'")
        print("2. Add reference images to: reference_images/persona1/")
        print("3. Train LoRA: ./scripts/train_lora.sh persona-your_name")
        print("4. Start ComfyUI: ./scripts/run_comfyui.sh")
        print("5. Load workflow: ADAPTIVE_BATCH_COMMUNITY_GENERATOR.json")
        print("\n📚 Documentation: docs/HOW_TO_USE_PERSONAS.md")
    else:
        print("⚠️  INSTALLATION INCOMPLETE")
        print("❌ Some components are missing or misconfigured")
        print("\n🔧 Recommended Actions:")
        print("1. Run: ./setup.sh")
        print("2. Run: ./scripts/download_models.sh") 
        print("3. Check error messages above")
        print("4. Consult documentation in docs/")
    
    print(f"\n{'='*70}")
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
