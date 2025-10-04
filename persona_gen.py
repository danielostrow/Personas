#!/usr/bin/env python3
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm

console = Console()

class PersonaGenerator:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.models_dir = project_root / "models"
        self.outputs_dir = project_root / "outputs"
        self.workflows_dir = project_root / "workflows"
        self.comfyui_dir = project_root / "ComfyUI"
        
    def create_workflow(self, persona_id: str, workflow_type: str = "image") -> Dict[str, Any]:
        """Create ComfyUI workflow for persona generation"""
        
        # Import persona manager
        from scripts.persona_manager import PersonaManager
        manager = PersonaManager(self.project_root)
        persona = manager.get_persona(persona_id)
        
        if not persona:
            raise ValueError(f"Persona {persona_id} not found")
        
        if not persona['trained']:
            raise ValueError(f"Persona {persona_id} is not trained yet")
        
        trigger_word = persona['trigger_word']
        lora_file = persona['lora_file']
        
        if workflow_type == "image":
            workflow = {
                "1": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {
                        "ckpt_name": "sd_xl_base_1.0.safetensors"
                    }
                },
                "2": {
                    "class_type": "LoraLoader",
                    "inputs": {
                        "lora_name": lora_file,
                        "strength_model": 0.8,
                        "strength_clip": 0.8,
                        "model": ["1", 0],
                        "clip": ["1", 1]
                    }
                },
                "3": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "text": f"masterpiece, best quality, ultra-detailed, {trigger_word}, portrait, professional photography",
                        "clip": ["2", 1]
                    }
                },
                "4": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "text": "low quality, bad anatomy, blurry, distorted",
                        "clip": ["2", 1]
                    }
                },
                "5": {
                    "class_type": "KSampler",
                    "inputs": {
                        "seed": 42,
                        "steps": 30,
                        "cfg": 7.5,
                        "sampler_name": "euler_a",
                        "scheduler": "normal",
                        "denoise": 1.0,
                        "model": ["2", 0],
                        "positive": ["3", 0],
                        "negative": ["4", 0],
                        "latent_image": ["6", 0]
                    }
                },
                "6": {
                    "class_type": "EmptyLatentImage",
                    "inputs": {
                        "width": 1024,
                        "height": 1024,
                        "batch_size": 1
                    }
                },
                "7": {
                    "class_type": "VAEDecode",
                    "inputs": {
                        "samples": ["5", 0],
                        "vae": ["1", 2]
                    }
                },
                "8": {
                    "class_type": "SaveImage",
                    "inputs": {
                        "filename_prefix": f"{persona_id}_output",
                        "images": ["7", 0]
                    }
                }
            }
        else:  # video workflow
            workflow = self._create_video_workflow(persona_id, trigger_word, lora_file)
        
        return workflow
    
    def _create_video_workflow(self, persona_id: str, trigger_word: str, lora_file: str) -> Dict[str, Any]:
        """Create video generation workflow"""
        # Complex video workflow with AnimateDiff
        return {
            # Base model and LoRA loading (similar to image)
            "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
            "2": {"class_type": "LoraLoader", "inputs": {
                "lora_name": lora_file,
                "strength_model": 0.8,
                "strength_clip": 0.8,
                "model": ["1", 0],
                "clip": ["1", 1]
            }},
            # AnimateDiff loader
            "10": {
                "class_type": "ADE_LoadAnimateDiffModel",
                "inputs": {
                    "model_name": "mm_sd_v15_v2.ckpt"
                }
            },
            "11": {
                "class_type": "ADE_ApplyAnimateDiffModel",
                "inputs": {
                    "model": ["2", 0],
                    "motion_model": ["10", 0],
                    "beta_schedule": "linear"
                }
            },
            # Text encoding
            "3": {"class_type": "CLIPTextEncode", "inputs": {
                "text": f"masterpiece, cinematic, {trigger_word}, walking, dynamic motion",
                "clip": ["2", 1]
            }},
            "4": {"class_type": "CLIPTextEncode", "inputs": {
                "text": "static, blurry, distorted",
                "clip": ["2", 1]
            }},
            # Batch latent for video frames
            "12": {
                "class_type": "ADE_EmptyLatentImageLarge",
                "inputs": {
                    "width": 768,
                    "height": 768,
                    "batch_size": 16  # 16 frames
                }
            },
            # KSampler for video
            "13": {
                "class_type": "KSampler",
                "inputs": {
                    "seed": 42,
                    "steps": 25,
                    "cfg": 7.5,
                    "sampler_name": "euler_a",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["11", 0],
                    "positive": ["3", 0],
                    "negative": ["4", 0],
                    "latent_image": ["12", 0]
                }
            },
            # VAE Decode
            "14": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": ["13", 0],
                    "vae": ["1", 2]
                }
            },
            # Video combine
            "15": {
                "class_type": "ADE_VideoCombine",
                "inputs": {
                    "images": ["14", 0],
                    "frame_rate": 8,
                    "format": "mp4",
                    "filename_prefix": f"{persona_id}_video"
                }
            }
        }
    
    def save_workflow(self, workflow: Dict[str, Any], name: str):
        """Save workflow to file"""
        self.workflows_dir.mkdir(exist_ok=True)
        workflow_file = self.workflows_dir / f"{name}.json"
        with open(workflow_file, 'w') as f:
            json.dump(workflow, f, indent=2)
        console.print(f"[green]Workflow saved to: {workflow_file}[/green]")
        return workflow_file

@click.group()
def cli():
    """Persona Generation CLI - Manage your AI personas"""
    pass

@cli.command()
@click.option('--persona-id', required=True, help='Persona ID (e.g., persona-john)')
@click.option('--type', type=click.Choice(['image', 'video']), default='image', help='Workflow type')
def create_workflow(persona_id, type):
    """Create a ComfyUI workflow for persona generation"""
    project_root = Path(__file__).parent
    generator = PersonaGenerator(project_root)
    
    try:
        workflow = generator.create_workflow(persona_id, type)
        workflow_file = generator.save_workflow(workflow, f"{persona_id}_{type}_workflow")
        
        console.print(f"\n[bold green]Workflow created successfully![/bold green]")
        console.print(f"Load this workflow in ComfyUI: {workflow_file}")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

@cli.command()
def list_models():
    """List all available models"""
    project_root = Path(__file__).parent
    models_dir = project_root / "models"
    
    table = Table(title="Available Models")
    table.add_column("Type", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Size", style="yellow")
    
    for model_type in ["checkpoints", "loras", "controlnet", "vae"]:
        type_dir = models_dir / model_type
        if type_dir.exists():
            for model_file in type_dir.glob("*"):
                if model_file.is_file():
                    size = model_file.stat().st_size / (1024 * 1024)  # MB
                    table.add_row(model_type, model_file.name, f"{size:.1f} MB")
    
    console.print(table)

@cli.command()
@click.option('--persona-id', required=True, help='Persona ID (e.g., persona-john)')
@click.option('--learning-rate', default=1e-4, help='Learning rate')
@click.option('--steps', default=4000, help='Training steps')
def train(persona_id, learning_rate, steps):
    """Train a LoRA for your persona"""
    project_root = Path(__file__).parent
    script_path = project_root / "scripts" / "train_lora.sh"
    
    if not script_path.exists():
        console.print("[red]Training script not found![/red]")
        return
    
    # Check if persona exists
    from scripts.persona_manager import PersonaManager
    manager = PersonaManager(project_root)
    persona = manager.get_persona(persona_id)
    
    if not persona:
        console.print(f"[red]Persona {persona_id} not found![/red]")
        console.print("[yellow]Use: python scripts/persona_manager.py add --name 'Your Name'[/yellow]")
        return
    
    # Check for training data
    training_data = Path(persona['training_data_path']) / "processed"
    if not training_data.exists() or not any(training_data.iterdir()):
        console.print("[yellow]No processed training data found![/yellow]")
        if Confirm.ask("Would you like to process raw images first?"):
            prepare_script = project_root / "scripts" / "prepare_training_data.py"
            subprocess.run(["python", str(prepare_script), "--persona-id", persona_id])
    
    console.print(f"[green]Starting training for {persona['name']} ({persona_id})...[/green]")
    subprocess.run(["bash", str(script_path), persona_id, str(learning_rate), str(steps)])

@cli.command()
def start_ui():
    """Start ComfyUI server"""
    project_root = Path(__file__).parent
    script_path = project_root / "scripts" / "run_comfyui.sh"
    
    if not script_path.exists():
        console.print("[red]ComfyUI script not found![/red]")
        return
    
    console.print("[green]Starting ComfyUI...[/green]")
    subprocess.run(["bash", str(script_path)])

@cli.command()
@click.option('--all', is_flag=True, help='Setup everything including model downloads')
def setup(all):
    """Run initial setup"""
    project_root = Path(__file__).parent
    setup_script = project_root / "setup.sh"
    
    console.print("[green]Running setup...[/green]")
    subprocess.run(["bash", str(setup_script)])
    
    if all:
        download_script = project_root / "scripts" / "download_models.sh"
        if download_script.exists():
            if Confirm.ask("Download all models? (This will take some time)"):
                subprocess.run(["bash", str(download_script)])

if __name__ == "__main__":
    cli()
