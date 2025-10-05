#!/usr/bin/env python3
import click
import json
from pathlib import Path
from rich.console import Console

console = Console()

@click.command()
@click.option('--persona-id', required=True, help='Persona ID to test')
@click.option('--strengths', default='0.6,0.7,0.8,0.9,1.0', help='Comma-separated LoRA strengths to test')
@click.option('--prompt', help='Custom prompt (optional)')
def test_lora_strengths(persona_id, strengths, prompt):
    """Create workflows to test different LoRA strengths"""
    
    project_root = Path(__file__).parent.parent
    
    # Import persona manager
    import sys
    sys.path.insert(0, str(project_root / "scripts"))
    from persona_manager import PersonaManager
    
    manager = PersonaManager(project_root)
    persona = manager.get_persona(persona_id)
    
    if not persona:
        console.print(f"[red]Error: Persona {persona_id} not found[/red]")
        return
    
    if not persona.get('trained', False):
        console.print(f"[red]Error: Persona {persona_id} is not trained yet[/red]")
        return
    
    trigger_word = persona['trigger_word']
    lora_file = persona['lora_file']
    
    # Default prompt if not provided
    if not prompt:
        prompt = f"masterpiece, professional portrait of {trigger_word}, detailed facial features, sharp focus, studio lighting, highly detailed"
    
    # Parse strengths
    strength_values = [float(s.strip()) for s in strengths.split(',')]
    
    console.print(f"[blue]Creating strength test workflows for {persona_id}[/blue]")
    console.print(f"[blue]Testing strengths: {strength_values}[/blue]")
    
    workflows_created = []
    
    for strength in strength_values:
        workflow_name = f"{persona_id}_strength_{strength}_test"
        workflow = create_strength_test_workflow(
            persona_id, trigger_word, lora_file, strength, prompt
        )
        
        # Save workflow
        workflow_file = project_root / "workflows" / f"{workflow_name}.json"
        with open(workflow_file, 'w') as f:
            json.dump(workflow, f, indent=2)
        
        # Also save to ComfyUI
        comfyui_workflow_dir = project_root / "ComfyUI" / "user" / "default" / "workflows"
        if comfyui_workflow_dir.exists():
            comfyui_workflow_file = comfyui_workflow_dir / f"{workflow_name}.json"
            with open(comfyui_workflow_file, 'w') as f:
                json.dump(workflow, f, indent=2)
        
        workflows_created.append(workflow_name)
        console.print(f"[green]✓ Created workflow for strength {strength}[/green]")
    
    console.print(f"\n[yellow]📋 Generated {len(workflows_created)} test workflows:[/yellow]")
    for workflow in workflows_created:
        console.print(f"  • {workflow}")
    
    console.print(f"\n[blue]🎯 Usage:[/blue]")
    console.print(f"1. Load each workflow in ComfyUI")
    console.print(f"2. Generate images with same seed")
    console.print(f"3. Compare results to find optimal strength")
    console.print(f"4. Update your main workflow with best strength")

def create_strength_test_workflow(persona_id, trigger_word, lora_file, strength, prompt):
    """Create a workflow with specific LoRA strength"""
    
    # Extract just the filename from lora_file path
    lora_filename = Path(lora_file).name if "/" in lora_file else lora_file
    
    workflow = {
        "last_node_id": 8,
        "last_link_id": 11,
        "nodes": [
            {
                "id": 1,
                "type": "CheckpointLoaderSimple",
                "pos": [50, 50],
                "size": [315, 98],
                "flags": {},
                "order": 0,
                "mode": 0,
                "outputs": [
                    {"name": "MODEL", "type": "MODEL", "links": [1], "slot_index": 0},
                    {"name": "CLIP", "type": "CLIP", "links": [2], "slot_index": 1},
                    {"name": "VAE", "type": "VAE", "links": [8], "slot_index": 2}
                ],
                "properties": {"Node name for S&R": "CheckpointLoaderSimple"},
                "widgets_values": ["sd_xl_base_1.0.safetensors"]
            },
            {
                "id": 2,
                "type": "LoraLoader",
                "pos": [400, 50],
                "size": [315, 126],
                "flags": {},
                "order": 1,
                "mode": 0,
                "inputs": [
                    {"name": "model", "type": "MODEL", "link": 1},
                    {"name": "clip", "type": "CLIP", "link": 2}
                ],
                "outputs": [
                    {"name": "MODEL", "type": "MODEL", "links": [3], "slot_index": 0},
                    {"name": "CLIP", "type": "CLIP", "links": [4, 5], "slot_index": 1}
                ],
                "properties": {"Node name for S&R": "LoraLoader"},
                "widgets_values": [lora_filename, strength, strength]
            },
            {
                "id": 3,
                "type": "CLIPTextEncode",
                "pos": [750, 50],
                "size": [400, 200],
                "flags": {},
                "order": 2,
                "mode": 0,
                "inputs": [{"name": "clip", "type": "CLIP", "link": 4}],
                "outputs": [{"name": "CONDITIONING", "type": "CONDITIONING", "links": [6], "slot_index": 0}],
                "properties": {"Node name for S&R": "CLIPTextEncode"},
                "widgets_values": [prompt]
            },
            {
                "id": 4,
                "type": "CLIPTextEncode",
                "pos": [750, 300],
                "size": [400, 200],
                "flags": {},
                "order": 3,
                "mode": 0,
                "inputs": [{"name": "clip", "type": "CLIP", "link": 5}],
                "outputs": [{"name": "CONDITIONING", "type": "CONDITIONING", "links": [7], "slot_index": 0}],
                "properties": {"Node name for S&R": "CLIPTextEncode"},
                "widgets_values": ["low quality, bad anatomy, blurry, distorted, deformed"]
            },
            {
                "id": 5,
                "type": "EmptyLatentImage",
                "pos": [400, 300],
                "size": [315, 106],
                "flags": {},
                "order": 4,
                "mode": 0,
                "outputs": [{"name": "LATENT", "type": "LATENT", "links": [9], "slot_index": 0}],
                "properties": {"Node name for S&R": "EmptyLatentImage"},
                "widgets_values": [1024, 1024, 1]
            },
            {
                "id": 6,
                "type": "KSampler",
                "pos": [1200, 50],
                "size": [315, 262],
                "flags": {},
                "order": 5,
                "mode": 0,
                "inputs": [
                    {"name": "model", "type": "MODEL", "link": 3},
                    {"name": "positive", "type": "CONDITIONING", "link": 6},
                    {"name": "negative", "type": "CONDITIONING", "link": 7},
                    {"name": "latent_image", "type": "LATENT", "link": 9}
                ],
                "outputs": [{"name": "LATENT", "type": "LATENT", "links": [10], "slot_index": 0}],
                "properties": {"Node name for S&R": "KSampler"},
                "widgets_values": [42, "fixed", 35, 7.0, "euler", "normal", 1.0]  # Fixed seed for comparison
            },
            {
                "id": 7,
                "type": "VAEDecode",
                "pos": [1550, 50],
                "size": [210, 46],
                "flags": {},
                "order": 6,
                "mode": 0,
                "inputs": [
                    {"name": "samples", "type": "LATENT", "link": 10},
                    {"name": "vae", "type": "VAE", "link": 8}
                ],
                "outputs": [{"name": "IMAGE", "type": "IMAGE", "links": [11], "slot_index": 0}],
                "properties": {"Node name for S&R": "VAEDecode"}
            },
            {
                "id": 8,
                "type": "SaveImage",
                "pos": [1800, 50],
                "size": [315, 270],
                "flags": {},
                "order": 7,
                "mode": 0,
                "inputs": [{"name": "images", "type": "IMAGE", "link": 11}],
                "properties": {"Node name for S&R": "SaveImage"},
                "widgets_values": [f"{persona_id}_strength_{strength}"]
            }
        ],
        "links": [
            [1, 1, 0, 2, 0, "MODEL"],
            [2, 1, 1, 2, 1, "CLIP"],
            [3, 2, 0, 6, 0, "MODEL"],
            [4, 2, 1, 3, 0, "CLIP"],
            [5, 2, 1, 4, 0, "CLIP"],
            [6, 3, 0, 6, 1, "CONDITIONING"],
            [7, 4, 0, 6, 2, "CONDITIONING"],
            [8, 1, 2, 7, 1, "VAE"],
            [9, 5, 0, 6, 3, "LATENT"],
            [10, 6, 0, 7, 0, "LATENT"],
            [11, 7, 0, 8, 0, "IMAGE"]
        ],
        "groups": [],
        "config": {},
        "extra": {},
        "version": 0.4
    }
    
    return workflow

if __name__ == "__main__":
    test_lora_strengths()
