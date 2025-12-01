@echo off
title Centisky - Install Dependencies
echo ====================================
echo   Centisky - Installing Dependencies
echo   Developed by @Benji-Xu with Windsurf
echo ====================================
echo.
pip install -r "%~dp0program\requirements.txt"
echo.
echo ====================================
echo   Installation Complete!
echo ====================================
pause
