#!/usr/bin/env python3
"""
AI Music Generator Studio - Ultimate Launcher
Complete system with all features integrated
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Print the startup banner"""
    print("🎵" * 60)
    print("🎵" + " " * 18 + "AI MUSIC GENERATOR STUDIO" + " " * 15 + "🎵")
    print("🎵" + " " * 20 + "Ultimate Music Creation" + " " * 17 + "🎵")
    print("🎵" * 60)

def check_system():
    """Check system requirements"""
    print("\n🔧 System Check:")
    print("-" * 40)
    
    # Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"❌ Python 3.8+ required (current: {python_version.major}.{python_version.minor})")
        return False
    
    # Essential files
    essential_files = [
        ("AI Model", "ai-music-aml/outputs/rnn/best.keras"),
        ("Vocabulary", "ai-music-aml/outputs/processed/vocab.json"),
        ("Token Mapping", "ai-music-aml/outputs/processed/itos.pkl"),
        ("Enhanced UI", "enhanced_music_studio.py"),
        ("Chord Generator", "enhanced_chord_generator.py"),
        ("Note Generator", "enhanced_note_generator.py")
    ]
    
    all_files_exist = True
    for name, path in essential_files:
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✅ {name}: {size:,} bytes")
        else:
            print(f"❌ {name}: Missing ({path})")
            all_files_exist = False
    
    # Python packages
    required_packages = [
        ("Streamlit", "streamlit"),
        ("TensorFlow", "tensorflow"), 
        ("NumPy", "numpy"),
        ("Music21", "music21"),
        ("Plotly", "plotly")
    ]
    
    all_packages_available = True
    for name, package in required_packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name}: Not installed")
            all_packages_available = False
    
    return all_files_exist and all_packages_available

def show_main_menu():
    """Show the main menu"""
    print("\n🎵 What would you like to do?")
    print("=" * 50)
    print("1. 🌐 Launch Enhanced Web UI (Full Interface)")
    print("2. 💻 Quick Command Examples")
    print("3. 🎵 Run Complete Demo")
    print("4. 🔧 Test All Components")
    print("5. 📚 Show Usage Guide")
    print("6. ❌ Exit")
    print("=" * 50)

def launch_enhanced_ui():
    """Launch the enhanced Streamlit UI"""
    print("\n🚀 Launching Enhanced Music Studio...")
    
    try:
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "enhanced_music_studio.py",
            "--server.port", "8502"
        ]
        
        print("⏳ Starting Streamlit server...")
        process = subprocess.Popen(cmd)
        
        # Wait for server startup
        time.sleep(4)
        
        if process.poll() is None:  # Process still running
            print("✅ Server started successfully!")
            print("\n🌐 Enhanced AI Music Studio is LIVE!")
            print("📱 URL: http://localhost:8502")
            
            # Open browser
            try:
                webbrowser.open("http://localhost:8502")
                print("🌍 Browser opened automatically!")
            except:
                print("💡 Please manually open: http://localhost:8502")
            
            print("\n🎵 Features Available:")
            print("   • 🧠 Advanced AI Generation")
            print("   • 🎼 Interactive Chord Builder")
            print("   • 🎹 Note & Scale Generator")
            print("   • 📊 Real-time Progress Tracking")
            print("   • 💾 Direct MIDI Downloads")
            
            print("\n🛑 Press Ctrl+C to stop the server")
            
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Shutting down server...")
                process.terminate()
                print("✅ Server stopped successfully!")
                
        else:
            print("❌ Failed to start server")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def show_quick_examples():
    """Show quick command examples"""
    print("\n💻 QUICK COMMAND EXAMPLES:")
    print("=" * 60)
    print()
    
    examples = [
        ("🧠 AI Generation", "py -3 advanced_music_gen.py 200 0.8 my_song.mid"),
        ("🎼 Pop Chords", "py -3 enhanced_chord_generator.py C Am F G"),
        ("🎷 Jazz Chords", "py -3 enhanced_chord_generator.py Dm7 G7 CM7 Am7"),
        ("🎹 Simple Melody", "py -3 enhanced_note_generator.py C4 E4 G4 C5"),
        ("🎼 Major Scale", "py -3 enhanced_note_generator.py --scale C4 major 8"),
        ("🔵 Blues Scale", "py -3 enhanced_note_generator.py --scale E4 blues 7"),
        ("🔧 System Test", "py -3 test_step_by_step.py")
    ]
    
    for desc, cmd in examples:
        print(f"{desc}:")
        print(f"   {cmd}")
        print()
    
    print("💡 Try any of these commands in your terminal!")

def run_demo():
    """Run the complete system demo"""
    print("\n🎵 Running Complete System Demo...")
    print("🚀 This will test all generation methods!")
    
    if os.path.exists("demo_complete_system.py"):
        os.system("py -3 demo_complete_system.py")
    else:
        print("❌ Demo script not found")

def test_components():
    """Test all system components"""
    print("\n🔧 Testing All Components...")
    
    if os.path.exists("test_step_by_step.py"):
        os.system("py -3 test_step_by_step.py")
    else:
        print("❌ Test script not found")

def show_usage_guide():
    """Show detailed usage guide"""
    print("\n📚 COMPLETE USAGE GUIDE:")
    print("=" * 60)
    print()
    
    print("🎵 GENERATION METHODS:")
    print("   1. 🧠 Advanced AI: Pure neural network generation")
    print("   2. 🎼 Chord-Based: Start with chord progressions")
    print("   3. 🎹 Note-Based: Start with melodies or scales")
    print("   4. 🎨 Style-Based: Generate in specific genres")
    print()
    
    print("⚙️ KEY PARAMETERS:")
    print("   🎼 Length: 50-500 tokens (50=short, 200=medium, 500=long)")
    print("   🎨 Creativity: 0.1-2.0 (0.5=safe, 1.0=balanced, 1.5=creative)")
    print()
    
    print("🎼 CHORD PROGRESSIONS:")
    print("   Pop: C - Am - F - G")
    print("   Rock: Em - C - G - D") 
    print("   Jazz: Dm7 - G7 - CM7 - Am7")
    print("   Blues: E7 - A7 - B7 - E7")
    print()
    
    print("🎹 MUSICAL SCALES:")
    print("   Major: Bright, happy sound")
    print("   Minor: Sad, melancholic sound")
    print("   Pentatonic: Simple, universal appeal")
    print("   Blues: Soulful, expressive")
    print("   Dorian: Modal, sophisticated")
    print()
    
    print("📁 OUTPUT FILES:")
    print("   • All files saved to 'outputs/' folder")
    print("   • Standard MIDI format (.mid)")
    print("   • Compatible with all music software")
    print("   • Typical size: 500-3000 bytes")
    print()
    
    print("💡 PRO TIPS:")
    print("   • Start with creativity 0.7 for good balance")
    print("   • Use chord progressions for structured songs")
    print("   • Try different scales for unique flavors")
    print("   • Longer sequences create fuller compositions")
    print("   • Layer multiple generations for complex pieces")

def main():
    """Main application function"""
    print_banner()
    
    # System check
    if not check_system():
        print("\n❌ System requirements not met!")
        print("💡 Please install missing components and try again.")
        input("\nPress Enter to exit...")
        return
    
    print("\n✅ All systems ready!")
    
    while True:
        show_main_menu()
        
        try:
            choice = input("\n🎯 Your choice (1-6): ").strip()
            
            if choice == "1":
                launch_enhanced_ui()
                
            elif choice == "2":
                show_quick_examples()
                
            elif choice == "3":
                run_demo()
                
            elif choice == "4":
                test_components()
                
            elif choice == "5":
                show_usage_guide()
                
            elif choice == "6":
                print("\n🎵 Thanks for using AI Music Generator Studio!")
                print("🚀 Keep creating amazing music! 🚀")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-6.")
            
            if choice in ["2", "3", "4", "5"]:
                input("\n⏎ Press Enter to return to main menu...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using AI Music Generator!")
            break

if __name__ == "__main__":
    main()