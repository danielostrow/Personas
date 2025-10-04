#!/usr/bin/env python3
"""
Test script to verify the persona generation system is set up correctly
"""
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
import subprocess

console = Console()

def check_requirement(name: str, check_func, required: bool = True) -> bool:
    """Check a single requirement"""
    try:
        result = check_func()
        if result:
            console.print(f"✅ {name}")
            return True
        else:
            if required:
                console.print(f"❌ {name} - Required")
            else:
                console.print(f"⚠️  {name} - Optional")
            return False
    except Exception as e:
        if required:
            console.print(f"❌ {name} - Error: {str(e)}")
        else:
            console.print(f"⚠️  {name} - Error: {str(e)}")
        return False

def main():
    console.print("[bold blue]Persona Generation System - Setup Test[/bold blue]\n")
    
    project_root = Path(__file__).parent
    all_good = True
    
    # Check Python version
    console.print("[yellow]Checking Python environment...[/yellow]")
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 9:
        console.print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        console.print(f"❌ Python {python_version.major}.{python_version.minor} (Need 3.9+)")
        all_good = False
    
    # Check virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        console.print("✅ Virtual environment active")
    else:
        console.print("⚠️  Virtual environment not active (recommended)")
    
    console.print("\n[yellow]Checking directories...[/yellow]")
    
    # Check required directories
    dirs_to_check = [
        ("models/checkpoints", True),
        ("models/loras", True),
        ("models/controlnet", True),
        ("models/vae", True),
        ("training_data", True),
        ("outputs", True),
        ("workflows", True),
        ("configs", True),
        ("ComfyUI", True),
        ("sd-scripts", True),
    ]
    
    for dir_path, required in dirs_to_check:
        full_path = project_root / dir_path
        if full_path.exists():
            console.print(f"✅ {dir_path}")
        else:
            if required:
                console.print(f"❌ {dir_path} - Missing")
                all_good = False
            else:
                console.print(f"⚠️  {dir_path} - Optional")
    
    console.print("\n[yellow]Checking models...[/yellow]")
    
    # Check for downloaded models
    models_to_check = [
        ("models/checkpoints/sd_xl_base_1.0.safetensors", "SDXL Base Model", True),
        ("models/checkpoints/sd_xl_refiner_1.0.safetensors", "SDXL Refiner", False),
        ("models/vae/sdxl_vae.safetensors", "SDXL VAE", True),
        ("models/animatediff/mm_sd_v15_v2.ckpt", "AnimateDiff", False),
        ("models/controlnet/control_v11p_sd15_openpose.pth", "ControlNet OpenPose", False),
    ]
    
    for model_path, model_name, required in models_to_check:
        full_path = project_root / model_path
        if full_path.exists():
            size_mb = full_path.stat().st_size / (1024 * 1024)
            console.print(f"✅ {model_name} ({size_mb:.1f} MB)")
        else:
            if required:
                console.print(f"❌ {model_name} - Required")
                all_good = False
            else:
                console.print(f"⚠️  {model_name} - Optional")
    
    console.print("\n[yellow]Checking Python packages...[/yellow]")
    
    # Check required packages
    packages_to_check = [
        ("torch", True),
        ("torchvision", True),
        ("transformers", True),
        ("diffusers", True),
        ("accelerate", True),
        ("safetensors", True),
        ("PIL", True),
        ("numpy", True),
        ("click", True),
        ("rich", True),
    ]
    
    for package_name, required in packages_to_check:
        try:
            __import__(package_name)
            console.print(f"✅ {package_name}")
        except ImportError:
            if required:
                console.print(f"❌ {package_name} - Required")
                all_good = False
            else:
                console.print(f"⚠️  {package_name} - Optional")
    
    # Check for MPS support
    console.print("\n[yellow]Checking hardware support...[/yellow]")
    try:
        import torch
        if torch.backends.mps.is_available():
            console.print("✅ Apple Metal Performance Shaders (MPS) available")
        else:
            console.print("⚠️  MPS not available - will use CPU")
    except:
        console.print("❌ Cannot check MPS support")
    
    # Check for personas
    console.print("\n[yellow]Checking personas...[/yellow]")
    personas_file = project_root / "personas.json"
    if personas_file.exists():
        try:
            import json
            with open(personas_file, 'r') as f:
                data = json.load(f)
                persona_count = len(data.get("personas", {}))
                if persona_count > 0:
                    console.print(f"✅ {persona_count} persona(s) registered")
                    
                    # Show persona table
                    table = Table(title="Registered Personas")
                    table.add_column("ID", style="cyan")
                    table.add_column("Name", style="green") 
                    table.add_column("Trained", style="yellow")
                    
                    for pid, pdata in data["personas"].items():
                        table.add_row(
                            pid,
                            pdata["name"],
                            "✅" if pdata["trained"] else "❌"
                        )
                    console.print(table)
                else:
                    console.print("⚠️  No personas registered yet")
        except Exception as e:
            console.print(f"❌ Error reading personas: {e}")
    else:
        console.print("⚠️  No personas registered yet")
    
    # Summary
    console.print(f"\n[bold]{'='*50}[/bold]")
    if all_good:
        console.print("[bold green]✅ System is ready![/bold green]")
        console.print("\nNext steps:")
        console.print("1. Create a persona: python scripts/persona_manager.py add --name 'Your Name'")
        console.print("2. Add training images to the persona's raw folder")
        console.print("3. Process images: python scripts/prepare_training_data.py --persona-id persona-your_name")
        console.print("4. Train: ./scripts/train_lora.sh persona-your_name")
        console.print("\n📚 Documentation:")
        console.print("- Complete guide: docs/HOW_TO_USE_PERSONAS.md")
        console.print("- Quick reference: docs/QUICK_REFERENCE.md")
        console.print("- Multi-persona guide: docs/MULTI_PERSONA_GUIDE.md")
    else:
        console.print("[bold red]❌ Some issues need to be fixed[/bold red]")
        console.print("\nTo fix:")
        console.print("1. Run: ./setup.sh")
        console.print("2. Download models: ./scripts/download_models.sh")
        console.print("3. Activate virtual environment: source venv/bin/activate")

if __name__ == "__main__":
    main()
