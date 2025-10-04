#!/usr/bin/env python3
import os
import shutil
from pathlib import Path
from PIL import Image
import click
from rich.console import Console
from rich.progress import track

console = Console()

def process_image(input_path: Path, output_path: Path, target_size: int = 1024):
    """Process and resize image for training"""
    try:
        img = Image.open(input_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Calculate aspect ratio preserving resize
        width, height = img.size
        aspect_ratio = width / height
        
        if width > height:
            new_width = target_size
            new_height = int(target_size / aspect_ratio)
        else:
            new_height = target_size
            new_width = int(target_size * aspect_ratio)
        
        # Resize with high quality
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create square canvas
        canvas = Image.new('RGB', (target_size, target_size), (255, 255, 255))
        
        # Paste image centered
        x_offset = (target_size - new_width) // 2
        y_offset = (target_size - new_height) // 2
        canvas.paste(img, (x_offset, y_offset))
        
        # Save processed image
        canvas.save(output_path, 'PNG', quality=95)
        return True
    except Exception as e:
        console.print(f"[red]Error processing {input_path}: {e}[/red]")
        return False

@click.command()
@click.option('--persona-id', required=True, help='Persona ID (e.g., persona-larry)')
@click.option('--target-size', default=1024, help='Target size for training images')
@click.option('--caption-template', help='Custom caption template (defaults to "a photo of {trigger_word}")')
def prepare_data(persona_id, target_size, caption_template):
    """Prepare training data for LoRA training"""
    # Get persona info
    from pathlib import Path as PathLib
    import sys
    script_dir = PathLib(__file__).parent
    sys.path.insert(0, str(script_dir))
    
    try:
        from persona_manager import PersonaManager
        project_root = script_dir.parent
        manager = PersonaManager(project_root)
        persona = manager.get_persona(persona_id)
        
        if not persona:
            console.print(f"[red]Persona {persona_id} not found![/red]")
            console.print("[yellow]Use: python scripts/persona_manager.py add --name 'Your Name'[/yellow]")
            return
    except ImportError as e:
        console.print(f"[red]Error importing persona manager: {e}[/red]")
        return
    
    # Set paths from persona config
    input_path = PathLib(persona['training_data_path']) / 'raw'
    output_path = PathLib(persona['training_data_path']) / 'processed'
    trigger_word = persona['trigger_word']
    
    # Use default caption template if not provided
    if not caption_template:
        caption_template = f"a photo of {trigger_word}"
    else:
        caption_template = caption_template.format(trigger_word=trigger_word)
    
    if not input_path.exists():
        console.print(f"[red]Input directory {input_path} does not exist![/red]")
        return
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    image_files = [f for f in input_path.iterdir() 
                   if f.suffix.lower() in image_extensions]
    
    if not image_files:
        console.print(f"[red]No images found in {input_path}![/red]")
        console.print(f"[yellow]Please add images to: {input_path}[/yellow]")
        return
    
    console.print(f"[green]Found {len(image_files)} images[/green]")
    console.print(f"[blue]Persona: {persona['name']} ({persona_id})[/blue]")
    console.print(f"[blue]Trigger word: {trigger_word}[/blue]")
    
    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Process images
    processed = 0
    for idx, img_file in enumerate(track(image_files, description="Processing images...")):
        output_file = output_path / f"{persona_id}_{idx:04d}.png"
        
        if process_image(img_file, output_file, target_size):
            # Create caption file
            caption_file = output_file.with_suffix('.txt')
            caption_file.write_text(caption_template)
            processed += 1
    
    console.print(f"[green]Successfully processed {processed}/{len(image_files)} images[/green]")
    console.print(f"[blue]Output saved to: {output_path}[/blue]")
    
    # Create metadata file
    metadata_file = output_path / 'metadata.txt'
    with open(metadata_file, 'w') as f:
        f.write(f"Persona ID: {persona_id}\n")
        f.write(f"Persona Name: {persona['name']}\n")
        f.write(f"Trigger Word: {trigger_word}\n")
        f.write(f"Total images: {processed}\n")
        f.write(f"Image size: {target_size}x{target_size}\n")
        f.write(f"Caption: {caption_template}\n")

if __name__ == '__main__':
    prepare_data()
