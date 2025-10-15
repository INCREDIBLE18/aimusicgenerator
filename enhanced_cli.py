#!/usr/bin/env python3
"""
Enhanced Music Generation CLI
Step-by-step testing and generation interface
"""

import os
import sys
import json
import time
from datetime import datetime

def print_header():
    """Print the main header"""
    print("=" * 80)
    print("🎵 AI MUSIC GENERATOR - ENHANCED CLI INTERFACE")
    print("=" * 80)
    print("🎼 Choose your generation mode and watch the step-by-step process")
    print("🎹 Full control over chords, notes, scales, and AI creativity")
    print("=" * 80)

def print_step(step_num, title, description=""):
    """Print a step with formatting"""
    print(f"\n🔄 Step {step_num}: {title}")
    if description:
        print(f"   {description}")
    print("-" * 50)

def test_imports():
    """Test all imports and show system status"""
    print_step(1, "Testing System Components")
    
    components = {}
    
    # Test basic imports
    try:
        import numpy as np
        components['numpy'] = "✅ NumPy available"
    except ImportError:
        components['numpy'] = "❌ NumPy missing"
    
    # Test TensorFlow
    try:
        import tensorflow as tf
        components['tensorflow'] = f"✅ TensorFlow {tf.__version__}"
    except ImportError:
        components['tensorflow'] = "❌ TensorFlow missing"
    
    # Test music21
    try:
        from music21 import stream, note, chord
        components['music21'] = "✅ Music21 available"
    except ImportError:
        components['music21'] = "❌ Music21 missing"
    
    # Test our generators
    try:
        from advanced_music_gen import generate_music
        components['ai_generator'] = "✅ AI Generator available"
    except ImportError as e:
        components['ai_generator'] = f"❌ AI Generator error: {e}"
    
    try:
        from chord_generator_v2 import generate_chord_progression_song
        components['chord_generator'] = "✅ Chord Generator available"
    except ImportError as e:
        components['chord_generator'] = f"❌ Chord Generator error: {e}"
    
    try:
        from enhanced_chord_generator import generate_from_chord_progression
        components['enhanced_chord'] = "✅ Enhanced Chord Generator available"
    except ImportError as e:
        components['enhanced_chord'] = f"❌ Enhanced Chord error: {e}"
    
    try:
        from enhanced_note_generator import generate_from_note_sequence
        components['enhanced_note'] = "✅ Enhanced Note Generator available"
    except ImportError as e:
        components['enhanced_note'] = f"❌ Enhanced Note error: {e}"
    
    # Display results
    for component, status in components.items():
        print(f"   {status}")
    
    return all("✅" in status for status in components.values())

def check_model_files():
    """Check if required model and data files exist"""
    print_step(2, "Checking AI Model and Data Files")
    
    files_to_check = {
        "AI Model": "ai-music-aml/outputs/rnn/best.keras",
        "Vocabulary": "ai-music-aml/outputs/processed/vocab.json", 
        "Token Mapping": "ai-music-aml/outputs/processed/itos.pkl",
        "Training Data": "ai-music-aml/outputs/processed/tokens.txt",
        "MIDI Songs": "midi_songs"
    }
    
    all_exist = True
    for name, path in files_to_check.items():
        if os.path.exists(path):
            if os.path.isdir(path):
                file_count = len([f for f in os.listdir(path) if f.endswith('.mid')])
                print(f"   ✅ {name}: {path} ({file_count} MIDI files)")
            else:
                size = os.path.getsize(path)
                size_mb = size / (1024 * 1024)
                print(f"   ✅ {name}: {path} ({size_mb:.1f} MB)")
        else:
            print(f"   ❌ {name}: {path} (missing)")
            all_exist = False
    
    return all_exist

def show_generation_menu():
    """Show the main generation menu"""
    print("\n🎵 GENERATION MODES:")
    print("   1. 🤖 AI-Only Generation (pure neural network)")
    print("   2. 🎼 Chord Progression Mode")
    print("   3. 🎹 Note Sequence Mode") 
    print("   4. 🎵 Scale-Based Generation")
    print("   5. 🔧 Test All Components")
    print("   6. 📊 System Information")
    print("   0. ❌ Exit")
    
def ai_generation_mode():
    """AI-only generation mode"""
    print_step(3, "AI-Only Music Generation")
    
    # Get parameters
    print("📝 Configure your generation:")
    try:
        length = int(input("   🎵 Sequence length (50-500): ") or "150")
        creativity = float(input("   🎨 Creativity level (0.1-2.0): ") or "1.0")
        filename = input("   📁 Output filename (without .mid): ") or f"ai_generated_{int(time.time())}"
    except ValueError:
        print("❌ Invalid input, using defaults")
        length, creativity, filename = 150, 1.0, f"ai_generated_{int(time.time())}"
    
    print(f"\n🎯 Generating {length} tokens with creativity {creativity}...")
    
    try:
        from advanced_music_gen import generate_music
        
        print_step(4, "Loading AI Model", "Loading neural network and vocabulary...")
        
        result = generate_music(
            length=length,
            temperature=creativity,
            output_file=f"{filename}.mid"
        )
        
        if result.get('success'):
            print_step(5, "✅ Generation Successful!")
            print(f"   📁 File: outputs/{filename}.mid")
            print(f"   📊 Tokens generated: {result.get('tokens_generated', 'N/A')}")
            print(f"   🎵 File size: {result.get('midi_info', {}).get('file_size', 'N/A')} bytes")
            print(f"   🎼 Musical elements: {result.get('midi_info', {}).get('total_elements', 'N/A')}")
            return True
        else:
            print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def chord_progression_mode():
    """Chord progression based generation"""
    print_step(3, "Chord Progression Music Generation")
    
    print("🎼 Available chords:")
    major_chords = ["C", "D", "E", "F", "G", "A", "B"]
    minor_chords = [f"{c}m" for c in major_chords]
    seventh_chords = [f"{c}7" for c in major_chords]
    
    print(f"   Major: {' '.join(major_chords)}")
    print(f"   Minor: {' '.join(minor_chords)}")  
    print(f"   7th: {' '.join(seventh_chords)}")
    print("   Common progressions: I-V-vi-IV, ii-V-I, vi-IV-I-V")
    
    # Get chord progression
    chord_input = input("\n🎼 Enter chord progression (space-separated): ").strip()
    if not chord_input:
        chord_input = "C Am F G"
        print(f"   Using default: {chord_input}")
    
    chords = chord_input.split()
    
    # Get parameters
    try:
        ai_length = int(input("   🤖 AI enhancement length (50-300): ") or "100")
        creativity = float(input("   🎨 Creativity level (0.1-2.0): ") or "0.8")
        filename = input("   📁 Output filename: ") or f"chord_{'_'.join(chords)}_{int(time.time())}"
    except ValueError:
        print("❌ Invalid input, using defaults")
        ai_length, creativity, filename = 100, 0.8, f"chord_{'_'.join(chords)}_{int(time.time())}"
    
    try:
        from enhanced_chord_generator import generate_from_chord_progression
        
        print_step(4, "Generating Chord-Based Music")
        print(f"   🎼 Chords: {' → '.join(chords)}")
        print(f"   🤖 AI enhancement: {ai_length} tokens")
        print(f"   🎨 Creativity: {creativity}")
        
        result = generate_from_chord_progression(
            chord_names=chords,
            chord_duration=1.0,
            ai_enhancement_length=ai_length,
            temperature=creativity,
            output_file=f"{filename}.mid"
        )
        
        if result.get('success'):
            print_step(5, "✅ Chord Generation Successful!")
            print(f"   📁 File: {result.get('output_path', 'N/A')}")
            print(f"   🎼 Chord tokens: {result.get('chord_tokens', 'N/A')}")
            print(f"   🤖 AI tokens: {result.get('ai_tokens', 'N/A')}")
            print(f"   📊 Total tokens: {result.get('total_tokens', 'N/A')}")
            return True
        else:
            print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def note_sequence_mode():
    """Note sequence based generation"""
    print_step(3, "Note Sequence Music Generation")
    
    print("🎹 Available notes:")
    print("   Notes: C4, D4, E4, F4, G4, A4, B4, C5, D5, E5, F5, G5, A5, B5")
    print("   Sharps/Flats: C#4, D#4, F#4, G#4, A#4, etc.")
    print("   Examples: C4 E4 G4 (C major chord), A4 C5 E5 (A minor chord)")
    
    # Get note sequence
    note_input = input("\n🎹 Enter note sequence (space-separated): ").strip()
    if not note_input:
        note_input = "C4 E4 G4 C5"
        print(f"   Using default: {note_input}")
    
    notes = note_input.split()
    
    # Get parameters
    try:
        ai_length = int(input("   🤖 AI enhancement length (50-300): ") or "100")
        creativity = float(input("   🎨 Creativity level (0.1-2.0): ") or "0.8")
        filename = input("   📁 Output filename: ") or f"notes_{'_'.join(notes)}_{int(time.time())}"
    except ValueError:
        print("❌ Invalid input, using defaults")
        ai_length, creativity, filename = 100, 0.8, f"notes_{'_'.join(notes)}_{int(time.time())}"
    
    try:
        from enhanced_note_generator import generate_from_note_sequence
        
        print_step(4, "Generating Note-Based Music")
        print(f"   🎹 Notes: {' → '.join(notes)}")
        print(f"   🤖 AI enhancement: {ai_length} tokens")
        print(f"   🎨 Creativity: {creativity}")
        
        result = generate_from_note_sequence(
            note_names=notes,
            note_duration=0.5,
            ai_enhancement_length=ai_length,
            temperature=creativity,
            output_file=f"{filename}.mid"
        )
        
        if result.get('success'):
            print_step(5, "✅ Note Generation Successful!")
            print(f"   📁 File: {result.get('output_path', 'N/A')}")
            print(f"   🎹 Note tokens: {result.get('note_tokens', 'N/A')}")
            print(f"   🤖 AI tokens: {result.get('ai_tokens', 'N/A')}")
            print(f"   📊 Total tokens: {result.get('total_tokens', 'N/A')}")
            return True
        else:
            print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def scale_generation_mode():
    """Generate music based on musical scales"""
    print_step(3, "Scale-Based Music Generation")
    
    scales = {
        "C Major": ["C4", "D4", "E4", "F4", "G4", "A4", "B4"],
        "A Minor": ["A4", "B4", "C5", "D5", "E5", "F5", "G5"], 
        "G Major": ["G4", "A4", "B4", "C5", "D5", "E5", "F#5"],
        "E Minor": ["E4", "F#4", "G4", "A4", "B4", "C5", "D5"],
        "F Major": ["F4", "G4", "A4", "Bb4", "C5", "D5", "E5"],
        "D Minor": ["D4", "E4", "F4", "G4", "A4", "Bb4", "C5"]
    }
    
    print("🎵 Available scales:")
    for i, (scale_name, notes) in enumerate(scales.items(), 1):
        print(f"   {i}. {scale_name}: {' '.join(notes)}")
    
    try:
        choice = int(input("\n🎵 Choose scale (1-6): ")) - 1
        if 0 <= choice < len(scales):
            scale_name = list(scales.keys())[choice]
            scale_notes = scales[scale_name]
        else:
            scale_name = "C Major"
            scale_notes = scales[scale_name]
            print(f"   Invalid choice, using {scale_name}")
    except ValueError:
        scale_name = "C Major"
        scale_notes = scales[scale_name]
        print(f"   Invalid input, using {scale_name}")
    
    try:
        ai_length = int(input("   🤖 AI enhancement length (50-300): ") or "150")
        creativity = float(input("   🎨 Creativity level (0.1-2.0): ") or "0.9")
        filename = input("   📁 Output filename: ") or f"scale_{scale_name.replace(' ', '_')}_{int(time.time())}"
    except ValueError:
        ai_length, creativity, filename = 150, 0.9, f"scale_{scale_name.replace(' ', '_')}_{int(time.time())}"
    
    # Use note sequence generator with scale notes
    try:
        from enhanced_note_generator import generate_from_note_sequence
        
        print_step(4, f"Generating {scale_name} Scale Music")
        print(f"   🎵 Scale: {' → '.join(scale_notes)}")
        print(f"   🤖 AI enhancement: {ai_length} tokens")
        print(f"   🎨 Creativity: {creativity}")
        
        result = generate_from_note_sequence(
            note_names=scale_notes,
            note_duration=0.25,  # Shorter notes for scales
            ai_enhancement_length=ai_length,
            temperature=creativity,
            output_file=f"{filename}.mid"
        )
        
        if result.get('success'):
            print_step(5, "✅ Scale Generation Successful!")
            print(f"   📁 File: {result.get('output_path', 'N/A')}")
            print(f"   🎵 Scale tokens: {result.get('note_tokens', 'N/A')}")
            print(f"   🤖 AI tokens: {result.get('ai_tokens', 'N/A')}")
            print(f"   📊 Total tokens: {result.get('total_tokens', 'N/A')}")
            return True
        else:
            print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_all_components():
    """Test all generation modes"""
    print_step(3, "Testing All Components")
    
    tests = [
        ("AI Generation", lambda: ai_generation_quick_test()),
        ("Chord Generation", lambda: chord_generation_quick_test()),
        ("Note Generation", lambda: note_generation_quick_test()),
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"   ❌ {test_name} failed: {e}")
            results[test_name] = False
    
    print_step(4, "Test Results Summary")
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {status}: {test_name}")
    
    return all(results.values())

def ai_generation_quick_test():
    """Quick AI generation test"""
    from advanced_music_gen import generate_music
    result = generate_music(
        length=50,
        temperature=1.0,
        output_file="test_ai.mid"
    )
    return result.get('success', False)

def chord_generation_quick_test():
    """Quick chord generation test"""
    from enhanced_chord_generator import generate_from_chord_progression
    result = generate_from_chord_progression(
        chord_names=["C", "Am"],
        chord_duration=1.0,
        ai_enhancement_length=30,
        temperature=0.8,
        output_file="test_chord.mid"
    )
    return result.get('success', False)

def note_generation_quick_test():
    """Quick note generation test"""
    from enhanced_note_generator import generate_from_note_sequence
    result = generate_from_note_sequence(
        note_names=["C4", "E4"],
        note_duration=0.5,
        ai_enhancement_length=30,
        temperature=0.8,
        output_file="test_note.mid"
    )
    return result.get('success', False)

def show_system_info():
    """Show comprehensive system information"""
    print_step(3, "System Information")
    
    # AI Model info
    model_path = "ai-music-aml/outputs/rnn/best.keras"
    if os.path.exists(model_path):
        model_size = os.path.getsize(model_path) / (1024*1024)
        print(f"   🧠 AI Model: {model_size:.1f} MB")
    
    # Vocabulary info
    vocab_path = "ai-music-aml/outputs/processed/vocab.json"
    if os.path.exists(vocab_path):
        with open(vocab_path, 'r') as f:
            vocab = json.load(f)
        print(f"   📚 Vocabulary: {len(vocab):,} tokens")
    
    # Training data
    tokens_path = "ai-music-aml/outputs/processed/tokens.txt"
    if os.path.exists(tokens_path):
        tokens_size = os.path.getsize(tokens_path) / 1024
        print(f"   📊 Training tokens: {tokens_size:.1f} KB")
    
    # MIDI files
    midi_dir = "midi_songs"
    if os.path.exists(midi_dir):
        midi_files = [f for f in os.listdir(midi_dir) if f.endswith('.mid')]
        print(f"   🎵 Training MIDIs: {len(midi_files)} files")
    
    # Generated files
    output_dir = "outputs"
    if os.path.exists(output_dir):
        output_files = [f for f in os.listdir(output_dir) if f.endswith('.mid')]
        print(f"   📁 Generated files: {len(output_files)} files")
        
        if output_files:
            print(f"   📂 Recent generations:")
            for file in output_files[-3:]:
                file_path = os.path.join(output_dir, file)
                file_size = os.path.getsize(file_path)
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                print(f"      🎵 {file} ({file_size} bytes, {mtime.strftime('%Y-%m-%d %H:%M')})")

def main():
    """Main CLI interface"""
    print_header()
    
    # System checks
    if not test_imports():
        print("\n❌ Some components are missing. Please install required dependencies.")
        return
    
    if not check_model_files():
        print("\n⚠️  Some model files are missing. AI generation may not work.")
        print("   Run training first if needed.")
    else:
        print("\n✅ All system components ready!")
    
    # Main loop
    while True:
        show_generation_menu()
        
        try:
            choice = input("\n🎵 Choose generation mode (0-6): ").strip()
            
            if choice == "0":
                print("\n👋 Thanks for using AI Music Generator!")
                break
            elif choice == "1":
                ai_generation_mode()
            elif choice == "2":
                chord_progression_mode()
            elif choice == "3":
                note_sequence_mode()
            elif choice == "4":
                scale_generation_mode()
            elif choice == "5":
                test_all_components()
            elif choice == "6":
                show_system_info()
            else:
                print("❌ Invalid choice. Please select 0-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        
        # Wait before next iteration
        input("\n⏸️  Press Enter to continue...")

if __name__ == "__main__":
    main()