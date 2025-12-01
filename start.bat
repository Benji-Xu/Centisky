@echo off
title Centisky
echo ====================================
echo   Centisky
echo   Developed by Benjamin with Windsurf
echo   GitHub: github.com/Benji-Xu
echo ====================================
echo.
echo Starting launcher...
cd /d "%~dp0program"
python launcher.py
if errorlevel 1 (
    echo.
    echo Failed to start! Make sure Python and dependencies are installed.
    echo.
    echo Install dependencies:
    echo pip install -r requirements.txt
    pause
)

