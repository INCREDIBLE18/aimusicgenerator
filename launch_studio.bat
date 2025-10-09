@echo off
echo ========================================
echo    AI Music Composer Studio Launcher
echo ========================================
echo.
echo Starting the Professional AI Music Composer Studio...
echo This will open in your web browser.
echo.
echo To stop the application, press Ctrl+C
echo.

cd /d "%~dp0"
cd ai-music-aml

echo Checking dependencies...
py -3 -c "import streamlit, plotly" 2>nul
if errorlevel 1 (
    echo Installing required dependencies...
    py -3 -m pip install plotly streamlit
)

echo.
echo Launching Professional AI Music Composer Studio...
echo.
py -3 -m streamlit run src/ui/professional_app.py --server.port 8501 --server.address localhost --server.headless true

echo.
echo Studio has been stopped.
pause