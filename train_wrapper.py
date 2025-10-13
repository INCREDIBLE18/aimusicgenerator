#!/usr/bin/env python3
"""
Training wrapper script to handle module import issues
"""
import os
import sys
import subprocess
from pathlib import Path
import time

def run_training(model_type="rnn", max_epochs=5):
    """Run training with proper path setup and progress output"""
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
        # Create a limited training config for faster testing
        print(f"🚀 Starting {model_type.upper()} training with {max_epochs} epochs...")
        
        if model_type == "rnn":
            from src.train_rnn import main
            # Modify config for shorter training
            import yaml
            with open("config.yaml", 'r') as f:
                config = yaml.safe_load(f)
            
            # Temporarily reduce epochs for testing
            original_epochs = config['train']['epochs']
            config['train']['epochs'] = max_epochs
            
            # Save temporary config
            with open("config_temp.yaml", 'w') as f:
                yaml.dump(config, f)
            
            print(f"📊 Training config: {max_epochs} epochs, batch size: {config['train']['batch_size']}")
            main("config_temp.yaml")  # Use temporary config
            
            # Clean up temp config
            if os.path.exists("config_temp.yaml"):
                os.remove("config_temp.yaml")
            
        elif model_type == "transformer":
            from src.train_transformer import main
            main("config.yaml")
        elif model_type == "gan":
            from src.train_gan import main
            main("config.yaml")
        else:
            print(f"Unknown model type: {model_type}")
            return False
        
        print(f"✅ {model_type.upper()} training completed successfully!")
        return True
        
    except KeyboardInterrupt:
        print(f"⏹️ Training interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False

if __name__ == "__main__":
    model_type = sys.argv[1] if len(sys.argv) > 1 else "rnn"
    max_epochs = int(sys.argv[2]) if len(sys.argv) > 2 else 5  # Default to 5 epochs for testing
    success = run_training(model_type, max_epochs)
    sys.exit(0 if success else 1)