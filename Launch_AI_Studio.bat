@echo off
title AI Music Composer Studio - Professional
echo ========================================
echo    AI Music Composer Studio
echo    Professional Edition
echo ========================================
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Navigate to ai-music-aml directory
if not exist "ai-music-aml" (
    echo ❌ Error: ai-music-aml directory not found!
    echo Please make sure you're running this from the correct location.
    pause
    exit /b 1
)

cd ai-music-aml

echo 📁 Current directory: %CD%
echo.

REM Check if Python is available
echo 🐍 Checking Python installation...
py -3 --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 not found!
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

py -3 --version
echo ✅ Python found!
echo.

REM Install/check dependencies
echo 📦 Installing dependencies...
py -3 -m pip install streamlit plotly --quiet
if errorlevel 1 (
    echo ⚠️  Warning: Some dependencies might not have installed correctly
)
echo ✅ Dependencies ready!
echo.

REM Start the application
echo 🚀 Starting AI Music Composer Studio...
echo 📱 The application will open in your browser
echo 🌐 URL: http://localhost:8501
echo.
echo 🛑 To stop the application, close this window or press Ctrl+C
echo ========================================
echo.

REM Open browser automatically after 3 seconds
start "" timeout /t 3 /nobreak >nul 2>&1 && start http://localhost:8501

REM Launch Streamlit
py -3 -m streamlit run src/ui/professional_app.py --server.port 8501 --server.headless true

echo.
echo 👋 AI Music Composer Studio has stopped.
pause