#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
import click
from rich.console import Console
import cv2
import numpy as np

console = Console()

class VideoProcessor:
    def __init__(self):
        self.ffmpeg_path = self._find_ffmpeg()
        
    def _find_ffmpeg(self):
        """Find ffmpeg executable"""
        try:
            result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return 'ffmpeg'  # Hope it's in PATH
    
    def interpolate_frames(self, input_video: Path, output_video: Path, target_fps: int = 24):
        """Frame interpolation using ffmpeg"""
        console.print(f"[yellow]Interpolating frames to {target_fps} FPS...[/yellow]")
        
        cmd = [
            self.ffmpeg_path,
            '-i', str(input_video),
            '-filter:v', f"minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps={target_fps}'",
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '18',
            str(output_video)
        ]
        
        try:
            subprocess.run(cmd, check=True)
            console.print(f"[green]Frame interpolation complete: {output_video}[/green]")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Frame interpolation failed: {e}[/red]")
            return False
    
    def upscale_video(self, input_video: Path, output_video: Path, scale: int = 2):
        """Basic upscaling using ffmpeg"""
        console.print(f"[yellow]Upscaling video {scale}x...[/yellow]")
        
        # Get video dimensions
        probe_cmd = [
            self.ffmpeg_path, '-i', str(input_video),
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'csv=s=x:p=0'
        ]
        
        try:
            result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
            width, height = map(int, result.stdout.strip().split('x'))
            new_width = width * scale
            new_height = height * scale
            
            # Upscale
            cmd = [
                self.ffmpeg_path,
                '-i', str(input_video),
                '-vf', f"scale={new_width}:{new_height}:flags=lanczos",
                '-c:v', 'libx264',
                '-preset', 'slow',
                '-crf', '18',
                str(output_video)
            ]
            
            subprocess.run(cmd, check=True)
            console.print(f"[green]Upscaling complete: {output_video}[/green]")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Upscaling failed: {e}[/red]")
            return False
    
    def enhance_colors(self, input_video: Path, output_video: Path):
        """Enhance colors and contrast"""
        console.print("[yellow]Enhancing colors...[/yellow]")
        
        cmd = [
            self.ffmpeg_path,
            '-i', str(input_video),
            '-vf', 'eq=contrast=1.1:brightness=0.05:saturation=1.2',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '18',
            str(output_video)
        ]
        
        try:
            subprocess.run(cmd, check=True)
            console.print(f"[green]Color enhancement complete: {output_video}[/green]")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Color enhancement failed: {e}[/red]")
            return False

@click.command()
@click.argument('input_video', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output video path')
@click.option('--interpolate', '-i', is_flag=True, help='Apply frame interpolation')
@click.option('--target-fps', default=24, help='Target FPS for interpolation')
@click.option('--upscale', '-u', is_flag=True, help='Upscale video')
@click.option('--scale-factor', default=2, help='Upscale factor')
@click.option('--enhance', '-e', is_flag=True, help='Enhance colors')
@click.option('--all', '-a', is_flag=True, help='Apply all enhancements')
def process_video(input_video, output, interpolate, target_fps, upscale, scale_factor, enhance, all):
    """Post-process generated videos"""
    input_path = Path(input_video)
    
    if not output:
        output_dir = input_path.parent / 'processed'
        output_dir.mkdir(exist_ok=True)
        output = output_dir / f"{input_path.stem}_processed{input_path.suffix}"
    
    output_path = Path(output)
    processor = VideoProcessor()
    
    # Check ffmpeg
    try:
        subprocess.run([processor.ffmpeg_path, '-version'], capture_output=True, check=True)
    except:
        console.print("[red]Error: ffmpeg not found. Install with: brew install ffmpeg[/red]")
        return
    
    current_input = input_path
    temp_files = []
    
    try:
        # Apply enhancements in sequence
        if all or interpolate:
            temp_output = output_path.parent / f"{output_path.stem}_interpolated{output_path.suffix}"
            if processor.interpolate_frames(current_input, temp_output, target_fps):
                current_input = temp_output
                temp_files.append(temp_output)
        
        if all or upscale:
            temp_output = output_path.parent / f"{output_path.stem}_upscaled{output_path.suffix}"
            if processor.upscale_video(current_input, temp_output, scale_factor):
                current_input = temp_output
                temp_files.append(temp_output)
        
        if all or enhance:
            if processor.enhance_colors(current_input, output_path):
                console.print(f"[bold green]Processing complete![/bold green]")
                console.print(f"[blue]Output saved to: {output_path}[/blue]")
        else:
            # Copy final result
            import shutil
            shutil.copy2(current_input, output_path)
            console.print(f"[bold green]Processing complete![/bold green]")
            console.print(f"[blue]Output saved to: {output_path}[/blue]")
        
    finally:
        # Cleanup temporary files
        for temp_file in temp_files[:-1]:  # Keep the last temp file as it's the output
            if temp_file.exists() and temp_file != output_path:
                temp_file.unlink()

if __name__ == '__main__':
    process_video()
