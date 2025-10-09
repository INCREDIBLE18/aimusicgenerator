#!/usr/bin/env python3
"""
AI Music Composer - Command Line Interface
Quick commands for common operations
"""

import argparse
import os
import sys
import subprocess
import yaml
from pathlib import Path

def load_config():
    """Load configuration file"""
    try:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def run_preprocessing(min_notes=50):
    """Run data preprocessing"""
    print("🔄 Starting data preprocessing...")
    try:
        cmd = f"python -m src.run_preprocess --config config.yaml --min_notes {min_notes}"
        result = subprocess.run(cmd, shell=True, check=True)
        print("✅ Data preprocessing completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Preprocessing failed: {e}")
        return False

def train_model(model_type="rnn"):
    """Train a model"""
    print(f"🧠 Starting {model_type.upper()} model training...")
    try:
        cmd = f"python -m src.train_{model_type} --config config.yaml"
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {model_type.upper()} model training completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Training failed: {e}")
        return False

def generate_music(model_type="rnn", length=200, temperature=1.0, output="generated_music.mid"):
    """Generate music"""
    print(f"🎵 Generating music with {model_type.upper()} model...")
    try:
        checkpoint = f"outputs/{model_type}/best.keras"
        if not os.path.exists(checkpoint):
            print(f"❌ Model not found: {checkpoint}")
            print(f"Please train the {model_type} model first!")
            return False
        
        output_path = f"outputs/{output}"
        cmd = f"python -m src.generate --checkpoint {checkpoint} --out {output_path} --config config.yaml"
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✅ Music generated: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Generation failed: {e}")
        return False

def launch_ui():
    """Launch the modern UI"""
    print("🚀 Launching AI Music Composer Studio...")
    try:
        cmd = "streamlit run src/ui/modern_app.py --server.port 8502"
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print("\n👋 UI closed!")

def show_status():
    """Show current system status"""
    print("📊 AI Music Composer Status")
    print("=" * 40)
    
    # Check MIDI files
    cfg = load_config()
    if cfg:
        midi_dir = cfg['data']['midi_dir']
        if os.path.exists(midi_dir):
            midi_files = [f for f in os.listdir(midi_dir) if f.endswith('.mid')]
            print(f"🎵 MIDI Files: {len(midi_files)} files in {midi_dir}")
        else:
            print(f"❌ MIDI directory not found: {midi_dir}")
    
    # Check processed data
    processed_tokens = "outputs/processed/tokens.txt"
    processed_vocab = "outputs/processed/vocab.json"
    if os.path.exists(processed_tokens) and os.path.exists(processed_vocab):
        try:
            with open(processed_tokens, 'r') as f:
                token_count = len(f.readlines())
            from src.utils.dataio import load_vocab
            vocab = load_vocab(processed_vocab)
            print(f"✅ Data Processed: {token_count} tokens, vocab size {len(vocab)}")
        except:
            print("⚠️  Data processed but unable to read details")
    else:
        print("❌ Data not processed")
    
    # Check models
    for model_type in ["rnn", "transformer"]:
        model_path = f"outputs/{model_type}/best.keras"
        if os.path.exists(model_path):
            size_mb = os.path.getsize(model_path) / (1024 * 1024)
            print(f"✅ {model_type.upper()} Model: Trained ({size_mb:.1f} MB)")
        else:
            print(f"❌ {model_type.upper()} Model: Not trained")
    
    # Check generated music
    gen_dir = "outputs"
    if os.path.exists(gen_dir):
        gen_files = [f for f in os.listdir(gen_dir) if f.endswith('.mid')]
        print(f"🎼 Generated Music: {len(gen_files)} files")
    else:
        print("🎼 Generated Music: None")
    
    print("=" * 40)

def quick_start():
    """Run the complete workflow"""
    print("🚀 AI Music Composer - Quick Start")
    print("This will run the complete workflow:")
    print("1. Process data")
    print("2. Train RNN model")
    print("3. Generate sample music")
    print()
    
    response = input("Continue? (y/N): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    # Step 1: Process data
    if not run_preprocessing():
        return
    
    print("\n" + "="*50)
    
    # Step 2: Train model
    if not train_model("rnn"):
        return
    
    print("\n" + "="*50)
    
    # Step 3: Generate music
    if not generate_music("rnn", length=150, output="quickstart_composition.mid"):
        return
    
    print("\n🎉 Quick start completed!")
    print("✅ Your AI composition is ready: outputs/quickstart_composition.mid")

def main():
    parser = argparse.ArgumentParser(description="AI Music Composer CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    subparsers.add_parser('status', help='Show system status')
    
    # Preprocess command
    preprocess_parser = subparsers.add_parser('preprocess', help='Process MIDI data')
    preprocess_parser.add_argument('--min-notes', type=int, default=50, 
                                 help='Minimum notes per file')
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train a model')
    train_parser.add_argument('--model', choices=['rnn', 'transformer'], default='rnn',
                            help='Model type to train')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate music')
    gen_parser.add_argument('--model', choices=['rnn', 'transformer'], default='rnn',
                          help='Model type to use')
    gen_parser.add_argument('--length', type=int, default=200,
                          help='Number of notes to generate')
    gen_parser.add_argument('--temperature', type=float, default=1.0,
                          help='Creativity level (0.1-2.0)')
    gen_parser.add_argument('--output', default='generated_music.mid',
                          help='Output filename')
    
    # UI command
    subparsers.add_parser('ui', help='Launch the modern web UI')
    
    # Quick start command
    subparsers.add_parser('quickstart', help='Run complete workflow')
    
    args = parser.parse_args()
    
    # Change to the correct directory
    if os.path.basename(os.getcwd()) != "ai-music-aml":
        if os.path.exists("ai-music-aml"):
            os.chdir("ai-music-aml")
        else:
            print("Error: Please run from the Music_Generator_Aiml directory")
            return
    
    if args.command == 'status':
        show_status()
    elif args.command == 'preprocess':
        run_preprocessing(args.min_notes)
    elif args.command == 'train':
        train_model(args.model)
    elif args.command == 'generate':
        generate_music(args.model, args.length, args.temperature, args.output)
    elif args.command == 'ui':
        launch_ui()
    elif args.command == 'quickstart':
        quick_start()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()