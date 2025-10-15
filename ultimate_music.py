#!/usr/bin/env python3
"""
Ultimate AI Music Generator
Combines all music generation features:
- Basic random generation
- Note-based generation  
- Chord progression generation
- Style and mood control
"""

import sys
import os
import json
import pickle
import numpy as np

def show_ultimate_usage():
    """Show comprehensive usage guide"""
    print("🎼 Ultimate AI Music Generator")
    print("=" * 60)
    print("\n🎵 Generation Modes:")
    print("  1. Basic:     py -3 ultimate_music.py basic [length] [creativity]")
    print("  2. Notes:     py -3 ultimate_music.py notes \"C4 E4 G4\" [length] [creativity]")
    print("  3. Chords:    py -3 ultimate_music.py chords \"C Am F G\" [length] [creativity]")
    print("  4. Style:     py -3 ultimate_music.py style jazz [length] [creativity]")
    print()
    print("🎹 Available Styles:")
    print("  pop, jazz, blues, rock, folk, classical, minor, sad, happy")
    print()
    print("📝 Examples:")
    print("  py -3 ultimate_music.py basic 200 1.0")
    print("  py -3 ultimate_music.py notes \"C4 E4 G4\" 150 0.8")
    print("  py -3 ultimate_music.py chords \"Cmaj7 Am7 Dm7 G7\" 300 1.2")
    print("  py -3 ultimate_music.py style jazz 250 0.9")
    print()
    print("⚙️ Parameters:")
    print("  mode: basic|notes|chords|style (required)")
    print("  input: Notes, chords, or style name")
    print("  length: 20-1000 tokens (default: 200)")
    print("  creativity: 0.1-2.0 (default: 1.0)")

def generate_ultimate_music(mode, input_data=None, length=200, creativity=1.0):
    """Generate music using the specified mode"""
    
    print(f"🎼 Ultimate AI Music Generator")
    print(f"🎵 Mode: {mode.upper()}")
    print(f"📏 Length: {length} tokens")
    print(f"🌡️ Creativity: {creativity}")
    print("=" * 50)
    
    if mode == "basic":
        return run_basic_generation(length, creativity)
    elif mode == "notes":
        return run_note_generation(input_data, length, creativity)
    elif mode == "chords":
        return run_chord_generation(input_data, length, creativity)
    elif mode == "style":
        return run_style_generation(input_data, length, creativity)
    else:
        print("❌ Unknown mode. Use: basic, notes, chords, or style")
        return False

def run_basic_generation(length, creativity):
    """Run basic random generation"""
    print("🎲 Generating random music...")
    
    output_file = f"ultimate_basic_{length}_{int(creativity*10)}.mid"
    
    try:
        # Import and run the basic generator
        import advanced_music_gen
        return advanced_music_gen.generate_music(
            length, creativity, output_file
        )
    except Exception as e:
        print(f"❌ Basic generation failed: {e}")
        return False

def run_note_generation(notes, length, creativity):
    """Run note-based generation"""
    print(f"🎵 Generating music from notes: {notes}")
    
    if not notes:
        print("❌ No notes provided")
        return False
    
    output_file = f"ultimate_notes_{length}_{int(creativity*10)}.mid"
    
    try:
        # Import and run the note generator
        import note_generator
        return note_generator.generate_with_seed_notes(
            notes, length, creativity, output_file
        )
    except Exception as e:
        print(f"❌ Note generation failed: {e}")
        return False

def run_chord_generation(chords, length, creativity):
    """Run chord progression generation"""
    print(f"🎹 Generating music from chords: {chords}")
    
    if not chords:
        print("❌ No chords provided")
        return False
    
    output_file = f"ultimate_chords_{length}_{int(creativity*10)}.mid"
    
    try:
        # Import and run the chord generator
        import chord_generator_v2
        return chord_generator_v2.generate_chord_progression_song(
            chords, length, creativity, 120, output_file
        )
    except Exception as e:
        print(f"❌ Chord generation failed: {e}")
        return False

def run_style_generation(style, length, creativity):
    """Run style-based generation"""
    print(f"🎼 Generating music in style: {style}")
    
    # Style to chord progression mapping
    style_progressions = {
        'pop': 'C Am F G',
        'jazz': 'Cmaj7 Am7 Dm7 G7',
        'blues': 'C7 F7 C7 G7',
        'rock': 'C G Am F',
        'folk': 'C F Am G',
        'classical': 'C G Am F C Dm G C',
        'minor': 'Am F C G',
        'sad': 'Am Dm G C',
        'happy': 'C F G C'
    }
    
    if style.lower() not in style_progressions:
        print(f"❌ Unknown style: {style}")
        print(f"Available styles: {', '.join(style_progressions.keys())}")
        return False
    
    chord_progression = style_progressions[style.lower()]
    output_file = f"ultimate_{style}_{length}_{int(creativity*10)}.mid"
    
    try:
        # Import and run the chord generator with style
        import chord_generator_v2
        return chord_generator_v2.generate_chord_progression_song(
            chord_progression, length, creativity, 120, output_file
        )
    except Exception as e:
        print(f"❌ Style generation failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_ultimate_usage()
        sys.exit(1)
    
    # Parse arguments
    mode = sys.argv[1].lower()
    
    if mode in ['basic']:
        input_data = None
        length = int(sys.argv[2]) if len(sys.argv) > 2 else 200
        creativity = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    elif mode in ['notes', 'chords', 'style']:
        if len(sys.argv) < 3:
            print(f"❌ {mode.title()} mode requires input data")
            show_ultimate_usage()
            sys.exit(1)
        input_data = sys.argv[2]
        length = int(sys.argv[3]) if len(sys.argv) > 3 else 200
        creativity = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    else:
        print(f"❌ Unknown mode: {mode}")
        show_ultimate_usage()
        sys.exit(1)
    
    # Validate parameters
    if length < 20 or length > 1000:
        print("❌ Length must be between 20 and 1000")
        sys.exit(1)
    
    if creativity < 0.1 or creativity > 2.0:
        print("❌ Creativity must be between 0.1 and 2.0")
        sys.exit(1)
    
    # Generate music
    success = generate_ultimate_music(mode, input_data, length, creativity)
    sys.exit(0 if success else 1)