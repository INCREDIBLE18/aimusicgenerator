#!/usr/bin/env python3
"""
AI Music Composer Studio - Professional Setup Script
This script sets up the complete environment and fixes all issues
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def setup_environment():
    """Set up the complete AI Music Composer environment"""
    print("🎵 AI Music Composer Studio - Professional Setup")
    print("=" * 55)
    
    # Get the correct paths
    script_dir = Path(__file__).parent
    ai_music_dir = script_dir / "ai-music-aml"
    
    print(f"📁 Project root: {script_dir}")
    print(f"📁 AI Music directory: {ai_music_dir}")
    
    # Step 1: Create necessary directories
    print("\n📂 Creating directory structure...")
    directories = [
        ai_music_dir / "outputs",
        ai_music_dir / "outputs" / "processed", 
        ai_music_dir / "outputs" / "rnn",
        ai_music_dir / "outputs" / "transformer",
        ai_music_dir / "outputs" / "generated",
        script_dir / "midi_songs"
    ]
    
    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ {dir_path.name}")
    
    # Step 2: Install dependencies
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", 
                       str(ai_music_dir / "requirements.txt")], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("⚠️  Some dependencies may have failed to install")
    
    # Step 3: Fix configuration
    print("\n⚙️  Setting up configuration...")
    config_path = ai_music_dir / "config.yaml"
    
    if config_path.exists():
        # Update MIDI directory path in config
        with open(config_path, 'r') as f:
            config_content = f.read()
        
        # Fix the MIDI directory path
        midi_dir_path = str(script_dir / "midi_songs").replace("\\", "/")
        config_content = config_content.replace(
            "midi_dir: d:/Music_Generator_Aiml/midi_songs",
            f"midi_dir: {midi_dir_path}"
        )
        
        with open(config_path, 'w') as f:
            f.write(config_content)
        
        print("✅ Configuration updated")
    else:
        print("⚠️  Configuration file not found")
    
    # Step 4: Clean up unnecessary files
    print("\n🧹 Cleaning up project...")
    cleanup_patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/src/ui/app.py",
        "**/src/ui/modern_app.py"
    ]
    
    for pattern in cleanup_patterns:
        for file_path in ai_music_dir.glob(pattern):
            if file_path.is_file():
                file_path.unlink()
                print(f"🗑️  Removed {file_path.name}")
            elif file_path.is_dir():
                shutil.rmtree(file_path)
                print(f"🗑️  Removed directory {file_path.name}")
    
    # Step 5: Create launcher scripts
    print("\n🚀 Creating launcher scripts...")
    
    # Windows batch launcher
    bat_content = f'''@echo off
title AI Music Composer Studio
echo ========================================
echo    AI Music Composer Studio - Professional
echo ========================================
echo.

cd /d "{ai_music_dir}"

echo Checking Python environment...
py -3 --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 not found. Please install Python 3.10 or higher.
    pause
    exit /b 1
)

echo Installing/updating dependencies...
py -3 -m pip install -r requirements.txt --quiet

echo.
echo 🚀 Starting AI Music Composer Studio...
echo 📱 Opening in your default browser...
echo 🛑 Press Ctrl+C to stop the server
echo.

start http://localhost:8501
py -3 -m streamlit run src/ui/professional_app.py --server.port 8501

echo.
echo 👋 AI Music Composer Studio stopped.
pause
'''
    
    launcher_path = script_dir / "Launch_AI_Music_Studio.bat"
    with open(launcher_path, 'w') as f:
        f.write(bat_content)
    print(f"✅ Created {launcher_path.name}")
    
    # Python launcher
    py_launcher_content = f'''#!/usr/bin/env python3
"""AI Music Composer Studio Launcher"""
import subprocess
import sys
import webbrowser
import time
import os
from pathlib import Path

def main():
    print("🎵 AI Music Composer Studio")
    print("=" * 40)
    
    # Change to correct directory
    ai_music_dir = Path(__file__).parent / "ai-music-aml"
    os.chdir(ai_music_dir)
    
    print(f"📁 Working directory: {{os.getcwd()}}")
    
    # Install dependencies
    print("📦 Checking dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies ready")
    except:
        print("⚠️  Warning: Some dependencies may be missing")
    
    # Start browser after delay
    def open_browser():
        time.sleep(3)
        webbrowser.open("http://localhost:8501")
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Launch app
    print("🚀 Starting AI Music Composer Studio...")
    print("📱 Will open in browser at http://localhost:8501")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 40)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", 
                       "src/ui/professional_app.py", "--server.port", "8501"])
    except KeyboardInterrupt:
        print("\\n👋 Goodbye!")

if __name__ == "__main__":
    main()
'''
    
    py_launcher_path = script_dir / "launch_ai_music_studio.py"
    with open(py_launcher_path, 'w') as f:
        f.write(py_launcher_content)
    print(f"✅ Created {py_launcher_path.name}")
    
    # Step 6: Create README
    print("\n📖 Creating documentation...")
    readme_content = f'''# 🎵 AI Music Composer Studio - Professional Edition

## 🚀 Quick Start

### Windows (Easy)
Double-click: `Launch_AI_Music_Studio.bat`

### Cross-Platform
```bash
python launch_ai_music_studio.py
```

### Manual
```bash
cd ai-music-aml
py -3 -m streamlit run src/ui/professional_app.py
```

Then open: http://localhost:8501

## ✨ Features

- 🎵 **Professional UI** with file upload
- 📁 **File Manager** for MIDI uploads
- 📊 **Data Processing** with progress tracking  
- 🧠 **Model Training** (RNN, Transformer, GAN)
- 🎼 **Music Generation** with style controls
- 🎵 **Music Testing** with custom files
- ⚙️ **Complete Settings** management
- 📖 **Built-in Help** system

## 📋 Requirements

- Python 3.10+
- 4GB+ RAM
- 2GB+ free disk space

## 🎯 Workflow

1. **📁 Upload MIDI files** in File Manager
2. **📊 Process data** to create training tokens
3. **🧠 Train AI model** (RNN recommended)
4. **🎵 Generate music** with trained model
5. **📥 Download** your AI compositions!

## 🔧 Troubleshooting

- **Can't start**: Install Python 3.10+ from python.org
- **Import errors**: Run `pip install -r requirements.txt`
- **No music generated**: Check if model is trained
- **UI issues**: Try different browser or port

---
**🎵 Enjoy creating AI music! ✨**
'''
    
    readme_path = script_dir / "README_PROFESSIONAL.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    print(f"✅ Created {readme_path.name}")
    
    # Final summary
    print("\n" + "=" * 55)
    print("🎉 Setup Complete!")
    print("=" * 55)
    print(f"📁 Project location: {script_dir}")
    print(f"🚀 To start: Double-click 'Launch_AI_Music_Studio.bat'")
    print(f"🌐 Or open: http://localhost:8501 after running launcher")
    print(f"📖 Read: README_PROFESSIONAL.md for full guide")
    print("=" * 55)
    
    return True

if __name__ == "__main__":
    setup_environment()