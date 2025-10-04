#!/usr/bin/env python3
import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import click
from rich.console import Console
from rich.table import Table
from datetime import datetime

console = Console()

class PersonaManager:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.personas_file = project_root / "personas.json"
        self.models_dir = project_root / "models" / "loras"
        self.training_data_dir = project_root / "training_data"
        self.personas = self._load_personas()
    
    def _load_personas(self) -> Dict:
        """Load personas from JSON file"""
        if self.personas_file.exists():
            with open(self.personas_file, 'r') as f:
                return json.load(f)
        return {"personas": {}}
    
    def _save_personas(self):
        """Save personas to JSON file"""
        with open(self.personas_file, 'w') as f:
            json.dump(self.personas, f, indent=2)
    
    def add_persona(self, name: str, description: str = "", trigger_word: str = None) -> str:
        """Add a new persona"""
        persona_id = f"persona-{name.lower().replace(' ', '_')}"
        trigger = trigger_word or persona_id
        
        if persona_id in self.personas["personas"]:
            raise ValueError(f"Persona {persona_id} already exists")
        
        self.personas["personas"][persona_id] = {
            "name": name,
            "description": description,
            "trigger_word": trigger,
            "created": datetime.now().isoformat(),
            "trained": False,
            "lora_file": None,
            "training_data_path": str(self.training_data_dir / persona_id),
            "config": {
                "base_model": "sd_xl_base_1.0.safetensors",
                "learning_rate": 1e-4,
                "train_steps": 4000,
                "network_dim": 64
            }
        }
        
        # Create directories
        (self.training_data_dir / persona_id / "raw").mkdir(parents=True, exist_ok=True)
        (self.training_data_dir / persona_id / "processed").mkdir(parents=True, exist_ok=True)
        
        self._save_personas()
        return persona_id
    
    def update_persona(self, persona_id: str, **kwargs):
        """Update persona information"""
        if persona_id not in self.personas["personas"]:
            raise ValueError(f"Persona {persona_id} not found")
        
        persona = self.personas["personas"][persona_id]
        for key, value in kwargs.items():
            if key == "config":
                persona["config"].update(value)
            else:
                persona[key] = value
        
        self._save_personas()
    
    def get_persona(self, persona_id: str) -> Optional[Dict]:
        """Get persona information"""
        return self.personas["personas"].get(persona_id)
    
    def list_personas(self) -> List[Dict]:
        """List all personas"""
        return [
            {"id": pid, **pdata} 
            for pid, pdata in self.personas["personas"].items()
        ]
    
    def mark_trained(self, persona_id: str, lora_file: str):
        """Mark persona as trained"""
        self.update_persona(
            persona_id,
            trained=True,
            lora_file=lora_file,
            trained_at=datetime.now().isoformat()
        )
    
    def generate_multi_lora_workflow(self, persona_ids: List[str], base_prompt: str) -> Dict:
        """Generate workflow with multiple LoRAs"""
        workflow = {
            "1": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": "sd_xl_base_1.0.safetensors"
                }
            }
        }
        
        # Chain LoRA loaders
        prev_model_node = "1"
        prev_model_output = 0
        prev_clip_output = 1
        
        for i, persona_id in enumerate(persona_ids, start=2):
            persona = self.get_persona(persona_id)
            if not persona or not persona["trained"]:
                console.print(f"[yellow]Warning: {persona_id} not trained, skipping[/yellow]")
                continue
            
            node_id = str(i)
            workflow[node_id] = {
                "class_type": "LoraLoader",
                "inputs": {
                    "lora_name": persona["lora_file"],
                    "strength_model": 0.7,  # Reduced strength for multiple LoRAs
                    "strength_clip": 0.7,
                    "model": [prev_model_node, prev_model_output],
                    "clip": [prev_model_node, prev_clip_output]
                }
            }
            prev_model_node = node_id
            prev_model_output = 0
            prev_clip_output = 1
        
        # Continue with standard workflow
        next_id = len(persona_ids) + 2
        
        # Positive prompt with all trigger words
        triggers = " ".join([
            self.get_persona(pid)["trigger_word"] 
            for pid in persona_ids 
            if self.get_persona(pid) and self.get_persona(pid)["trained"]
        ])
        
        workflow[str(next_id)] = {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": f"{base_prompt} {triggers}",
                "clip": [prev_model_node, prev_clip_output]
            }
        }
        
        # Rest of the workflow
        workflow[str(next_id + 1)] = {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": "low quality, bad anatomy, blurry, distorted",
                "clip": [prev_model_node, prev_clip_output]
            }
        }
        
        workflow[str(next_id + 2)] = {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": 1024,
                "height": 1024,
                "batch_size": 1
            }
        }
        
        workflow[str(next_id + 3)] = {
            "class_type": "KSampler",
            "inputs": {
                "seed": 42,
                "steps": 30,
                "cfg": 7.5,
                "sampler_name": "euler_a",
                "scheduler": "normal",
                "denoise": 1.0,
                "model": [prev_model_node, prev_model_output],
                "positive": [str(next_id), 0],
                "negative": [str(next_id + 1), 0],
                "latent_image": [str(next_id + 2), 0]
            }
        }
        
        workflow[str(next_id + 4)] = {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": [str(next_id + 3), 0],
                "vae": ["1", 2]
            }
        }
        
        workflow[str(next_id + 5)] = {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": f"multi_persona_{'_'.join(persona_ids)}",
                "images": [str(next_id + 4), 0]
            }
        }
        
        # ComfyUI workflows are just the nodes at root level - no metadata needed
        return workflow

@click.group()
def cli():
    """Persona management CLI"""
    pass

@cli.command()
@click.option('--name', prompt='Persona name', help='Display name for the persona')
@click.option('--description', prompt='Description', default='', help='Description of the persona')
@click.option('--trigger-word', help='Custom trigger word (defaults to persona-<name>)')
def add(name, description, trigger_word):
    """Add a new persona"""
    project_root = Path(__file__).parent.parent
    manager = PersonaManager(project_root)
    
    try:
        persona_id = manager.add_persona(name, description, trigger_word)
        console.print(f"[green]✓ Created persona: {persona_id}[/green]")
        console.print(f"[blue]Training data directory: training_data/{persona_id}/raw/[/blue]")
        console.print(f"[yellow]Add 20-30 images to the raw directory before training[/yellow]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

@cli.command()
@click.argument('persona-id')
@click.option('--lora-file', required=True, help='Path to the trained LoRA file')
def mark_trained(persona_id, lora_file):
    """Mark a persona as trained with the LoRA file location"""
    project_root = Path(__file__).parent.parent
    manager = PersonaManager(project_root)
    
    try:
        manager.mark_trained(persona_id, lora_file)
        console.print(f"[green]✓ Marked {persona_id} as trained[/green]")
        console.print(f"[blue]LoRA file: {lora_file}[/blue]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

@cli.command()
def list():
    """List all personas"""
    project_root = Path(__file__).parent.parent
    manager = PersonaManager(project_root)
    
    personas = manager.list_personas()
    if not personas:
        console.print("[yellow]No personas found[/yellow]")
        return
    
    table = Table(title="Personas")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Trigger", style="yellow")
    table.add_column("Trained", style="magenta")
    table.add_column("Created", style="blue")
    
    for persona in personas:
        table.add_row(
            persona["id"],
            persona["name"],
            persona["trigger_word"],
            "✓" if persona["trained"] else "✗",
            persona["created"][:10]
        )
    
    console.print(table)

@cli.command()
@click.argument('persona_id')
def info(persona_id):
    """Show detailed info about a persona"""
    project_root = Path(__file__).parent.parent
    manager = PersonaManager(project_root)
    
    persona = manager.get_persona(persona_id)
    if not persona:
        console.print(f"[red]Persona {persona_id} not found[/red]")
        return
    
    console.print(f"\n[bold]Persona: {persona['name']}[/bold]")
    console.print(f"ID: {persona_id}")
    console.print(f"Trigger: {persona['trigger_word']}")
    console.print(f"Description: {persona['description']}")
    console.print(f"Trained: {'Yes' if persona['trained'] else 'No'}")
    if persona['trained']:
        console.print(f"LoRA File: {persona['lora_file']}")
    console.print(f"\nTraining Config:")
    for key, value in persona['config'].items():
        console.print(f"  {key}: {value}")

@cli.command()
@click.argument('persona_ids', nargs=-1, required=True)
@click.option('--prompt', '-p', default='masterpiece, best quality', help='Base prompt')
@click.option('--output', '-o', help='Output workflow file')
def generate_workflow(persona_ids, prompt, output):
    """Generate workflow for multiple personas"""
    project_root = Path(__file__).parent.parent
    manager = PersonaManager(project_root)
    
    workflow = manager.generate_multi_lora_workflow(list(persona_ids), prompt)
    
    if output:
        output_path = Path(output)
    else:
        output_path = project_root / "workflows" / f"multi_{'_'.join(persona_ids)}.json"
    
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(workflow, f, indent=2)
    
    console.print(f"[green]Workflow saved to: {output_path}[/green]")

if __name__ == "__main__":
    cli()
