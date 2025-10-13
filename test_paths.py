#!/usr/bin/env python3
"""
Quick test to verify path resolution for the UI
"""

import os
from pathlib import Path

# Simulate running from ai-music-aml/src/ui/
current_dir = Path(__file__).parent / "ai-music-aml" / "src" / "ui"
print(f"Simulated current dir: {current_dir}")

# Test path resolution logic
ui_project_root = current_dir.parent.parent.parent  # Back to Music_Generator_Aiml
config_file_path = ui_project_root / 'ai-music-aml' / 'config.yaml'

print(f"Project root: {ui_project_root}")
print(f"Config path: {config_file_path}")
print(f"Config exists: {config_file_path.exists()}")

# Test data paths
midi_dir_abs = str(ui_project_root / "midi_songs")
proc_dir_abs = str(ui_project_root / "ai-music-aml" / "outputs" / "processed")

print(f"MIDI dir: {midi_dir_abs}")
print(f"MIDI dir exists: {os.path.exists(midi_dir_abs)}")
print(f"Processed dir: {proc_dir_abs}")
print(f"Processed dir exists: {os.path.exists(proc_dir_abs)}")

# Check actual project structure
print(f"\nActual project root: {Path(__file__).parent}")
actual_config = Path(__file__).parent / "ai-music-aml" / "config.yaml"
print(f"Actual config path: {actual_config}")
print(f"Actual config exists: {actual_config.exists()}")