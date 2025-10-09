#!/usr/bin/env python3
"""
AI Music Composer Studio Launcher
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import plotly
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        return False

def install_dependencies():
    """Install missing dependencies"""
    print("Installing required dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
        return True
    except subprocess.CalledProcessError:
        print("Failed to install dependencies")
        return False

def main():
    print("=" * 50)
    print("    AI Music Composer Studio Launcher")
    print("=" * 50)
    print()
    
    # Change to the correct directory
    script_dir = Path(__file__).parent
    ai_music_dir = script_dir / "ai-music-aml"
    
    if not ai_music_dir.exists():
        print("Error: ai-music-aml directory not found!")
        print(f"Expected path: {ai_music_dir}")
        return
    
    os.chdir(ai_music_dir)
    print(f"Working directory: {os.getcwd()}")
    
    # Check dependencies
    if not check_dependencies():
        if not install_dependencies():
            print("Failed to install dependencies. Please install manually:")
            print("pip install plotly")
            return
    
    print()
    print("Starting AI Music Composer Studio...")
    print("This will open in your web browser at http://localhost:8501")
    print()
    print("To stop the application, press Ctrl+C")
    print("=" * 50)
    print()
    
    # Launch streamlit
    try:
        # Open browser after a short delay
        def open_browser():
            time.sleep(3)
            webbrowser.open("http://localhost:8501")
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/ui/modern_app.py", 
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\nShutting down AI Music Composer Studio...")
    except Exception as e:
        print(f"Error launching application: {e}")

if __name__ == "__main__":
    main()