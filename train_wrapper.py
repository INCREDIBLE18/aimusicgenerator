#!/usr/bin/env python3
"""
Training wrapper script to handle module import issues
"""
import os
import sys
import subprocess
from pathlib import Path

def run_training(model_type="rnn"):
    """Run training with proper path setup"""
    # Get the project root directory
    current_dir = Path(__file__).parent
    project_root = current_dir
    ai_music_dir = project_root / "ai-music-aml"
    
    print(f"Current dir: {current_dir}")
    print(f"Project root: {project_root}")
    print(f"AI music dir: {ai_music_dir}")
    
    # Verify the directory exists
    if not ai_music_dir.exists():
        print(f"❌ Directory not found: {ai_music_dir}")
        return False
    
    # Change to the ai-music-aml directory
    os.chdir(ai_music_dir)
    print(f"Changed to: {os.getcwd()}")
    
    # Add the project paths to Python path
    sys.path.insert(0, str(ai_music_dir))
    sys.path.insert(0, str(project_root))
    
    try:
        if model_type == "rnn":
            from src.train_rnn import main
            main("config.yaml")  # Pass config file path
        elif model_type == "transformer":
            from src.train_transformer import main
            main("config.yaml")  # Pass config file path
        elif model_type == "gan":
            from src.train_gan import main
            main("config.yaml")  # Pass config file path
        else:
            print(f"Unknown model type: {model_type}")
            return False
        
        print(f"✅ {model_type.upper()} training completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False

if __name__ == "__main__":
    model_type = sys.argv[1] if len(sys.argv) > 1 else "rnn"
    success = run_training(model_type)
    sys.exit(0 if success else 1)