#!/usr/bin/env python3
"""
AI Music Composer Studio - System Check
Quick verification that everything is set up correctly
"""

import os
import sys
from pathlib import Path

def check_system():
    print("🎵 AI Music Composer Studio - System Check")
    print("=" * 50)
    
    # Check working directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check if we're in the right place
    ai_music_dir = current_dir / "ai-music-aml"
    if ai_music_dir.exists():
        print("✅ ai-music-aml directory found")
    else:
        print("❌ ai-music-aml directory not found")
        return False
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version >= (3, 10):
        print("✅ Python version compatible")
    else:
        print("❌ Python 3.10+ required")
        return False
    
    # Check key files
    key_files = [
        ai_music_dir / "config.yaml",
        ai_music_dir / "requirements.txt", 
        ai_music_dir / "src" / "ui" / "professional_app.py",
        current_dir / "midi_songs"
    ]
    
    for file_path in key_files:
        if file_path.exists():
            print(f"✅ {file_path.name}")
        else:
            print(f"❌ {file_path.name} missing")
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    deps = ["streamlit", "plotly", "tensorflow", "numpy", "music21"]
    
    for dep in deps:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} (run: pip install {dep})")
    
    # Check MIDI files
    midi_dir = current_dir / "midi_songs"
    if midi_dir.exists():
        midi_files = list(midi_dir.glob("*.mid")) + list(midi_dir.glob("*.midi"))
        print(f"\n🎵 MIDI files: {len(midi_files)} found")
        if len(midi_files) > 0:
            print("✅ Dataset ready")
        else:
            print("⚠️  No MIDI files - upload some to get started")
    
    # Check processed data
    processed_dir = ai_music_dir / "outputs" / "processed"
    if processed_dir.exists():
        tokens_file = processed_dir / "tokens.txt"
        vocab_file = processed_dir / "vocab.json"
        
        if tokens_file.exists() and vocab_file.exists():
            print("✅ Data processed and ready")
        else:
            print("⚠️  Data not processed yet")
    else:
        print("⚠️  No processed data")
    
    # Check trained models
    models_dir = ai_music_dir / "outputs"
    if models_dir.exists():
        rnn_model = models_dir / "rnn" / "best.keras"
        transformer_model = models_dir / "transformer" / "best.keras"
        
        trained_models = 0
        if rnn_model.exists():
            print("✅ RNN model trained")
            trained_models += 1
        else:
            print("⚠️  RNN model not trained")
            
        if transformer_model.exists():
            print("✅ Transformer model trained")
            trained_models += 1
        else:
            print("⚠️  Transformer model not trained")
            
        if trained_models > 0:
            print(f"✅ {trained_models} model(s) ready for generation")
        else:
            print("⚠️  No models trained yet")
    
    print("\n" + "=" * 50)
    print("🚀 To start the application:")
    print("   Windows: Double-click 'Launch_AI_Studio.bat'")
    print("   Manual: py -3 -m streamlit run ai-music-aml/src/ui/professional_app.py")
    print("   URL: http://localhost:8501")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    check_system()