#!/usr/bin/env python3
"""
AI Music Generator - Complete Demo
Show all generation capabilities with examples
"""

import os
import sys
import time
from datetime import datetime

def print_header():
    print("🎵" * 25)
    print("🎵   AI MUSIC GENERATOR COMPLETE DEMO   🎵")
    print("🎵" * 25)
    print()

def print_section(title):
    print("\n" + "="*60)
    print(f"📋 {title}")
    print("="*60)

def run_demo_command(description, command):
    print(f"\n🚀 {description}")
    print(f"💻 Command: {command}")
    print("⏳ Running...")
    
    start_time = time.time()
    result = os.system(command)
    end_time = time.time()
    
    if result == 0:
        print(f"✅ Completed successfully in {end_time - start_time:.2f} seconds!")
    else:
        print(f"❌ Command failed with code {result}")
    
    return result == 0

def main():
    print_header()
    
    print("🎼 This demo will showcase all music generation capabilities:")
    print("   1. Advanced AI Generation")
    print("   2. Chord-Based Generation") 
    print("   3. Note-Based Generation")
    print("   4. Scale-Based Generation")
    print("   5. Step-by-Step Testing")
    
    input("\n🎵 Press Enter to start the demo...")
    
    # 1. Advanced AI Generation
    print_section("1. Advanced AI Generation")
    print("🧠 Using pure AI to generate music from trained patterns")
    
    success = run_demo_command(
        "Generate 150-token song with medium creativity",
        "py -3 advanced_music_gen.py 150 0.8 demo_ai_generation.mid"
    )
    
    if success:
        print("🎵 Output: outputs/demo_ai_generation.mid")
    
    # 2. Chord-Based Generation
    print_section("2. Chord-Based Generation")
    print("🎼 Starting with chord progressions and enhancing with AI")
    
    # Classic pop progression
    success = run_demo_command(
        "Generate music from C-Am-F-G chord progression",
        "py -3 enhanced_chord_generator.py C Am F G"
    )
    
    if success:
        print("🎵 Output: outputs/chord_C_Am_F_G.mid")
    
    # Jazz progression
    success = run_demo_command(
        "Generate jazz-style music with 7th chords",
        "py -3 enhanced_chord_generator.py Dm7 G7 CM7 Am7"
    )
    
    if success:
        print("🎵 Output: outputs/chord_Dm7_G7_CM7_Am7.mid")
    
    # 3. Note-Based Generation
    print_section("3. Note-Based Generation")
    print("🎹 Starting with specific melodies and enhancing with AI")
    
    # Simple melody
    success = run_demo_command(
        "Generate music from C-E-G-C melody",
        "py -3 enhanced_note_generator.py C4 E4 G4 C5"
    )
    
    if success:
        print("🎵 Output: outputs/melody_C4_E4_G4_C5.mid")
    
    # Complex melody
    success = run_demo_command(
        "Generate music from pentatonic melody",
        "py -3 enhanced_note_generator.py C4 D4 E4 G4 A4 C5"
    )
    
    if success:
        print("🎵 Output: outputs/melody_C4_D4_E4_G4_A4_C5.mid")
    
    # 4. Scale-Based Generation
    print_section("4. Scale-Based Generation")
    print("🎼 Generate music from musical scales")
    
    # Major scale
    success = run_demo_command(
        "Generate music from C major scale",
        "py -3 enhanced_note_generator.py --scale C4 major 8"
    )
    
    if success:
        print("🎵 Output: outputs/scale_C4_major.mid")
    
    # Minor scale
    success = run_demo_command(
        "Generate music from A minor scale",
        "py -3 enhanced_note_generator.py --scale A4 minor 8"
    )
    
    if success:
        print("🎵 Output: outputs/scale_A4_minor.mid")
    
    # Pentatonic scale
    success = run_demo_command(
        "Generate music from G pentatonic scale",
        "py -3 enhanced_note_generator.py --scale G4 pentatonic 6"
    )
    
    if success:
        print("🎵 Output: outputs/scale_G4_pentatonic.mid")
    
    # Blues scale
    success = run_demo_command(
        "Generate music from E blues scale",
        "py -3 enhanced_note_generator.py --scale E4 blues 7"
    )
    
    if success:
        print("🎵 Output: outputs/scale_E4_blues.mid")
    
    # 5. System Testing
    print_section("5. System Component Testing")
    print("🔧 Testing all system components step by step")
    
    success = run_demo_command(
        "Run comprehensive system tests",
        "py -3 test_step_by_step.py"
    )
    
    # Show generated files
    print_section("Generated Music Files")
    print("📁 All generated MIDI files:")
    
    try:
        files = os.listdir("outputs")
        midi_files = [f for f in files if f.endswith('.mid')]
        
        for i, file in enumerate(midi_files, 1):
            file_path = os.path.join("outputs", file)
            file_size = os.path.getsize(file_path)
            print(f"   {i:2}. {file} ({file_size} bytes)")
        
        print(f"\n🎵 Total generated files: {len(midi_files)}")
        
    except Exception as e:
        print(f"❌ Error listing files: {e}")
    
    # Final summary
    print("\n" + "🎵"*60)
    print("🎉 DEMO COMPLETE! 🎉")
    print("🎵"*60)
    print()
    print("🎼 What you can do now:")
    print("   🌐 Open Enhanced UI: http://localhost:8502")
    print("   🎵 Play generated MIDI files in any music player")
    print("   🔧 Customize parameters for your own music")
    print("   📊 Experiment with different scales and chords")
    print()
    print("💡 Command Examples:")
    print("   py -3 enhanced_chord_generator.py Em Am C D")
    print("   py -3 enhanced_note_generator.py --scale F# minor 8")
    print("   py -3 advanced_music_gen.py 200 1.2 experimental.mid")
    print()
    print("🚀 Ready to create your own AI music! 🚀")

if __name__ == "__main__":
    main()