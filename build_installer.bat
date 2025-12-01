@echo off
chcp 65001 >nul
title Centisky - Build Installer
echo ====================================
echo   Centisky - Building Installer
echo   Developed by @Benji-Xu with Windsurf
echo ====================================
echo.

echo Checking environment...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo Installing build tools...
pip install pyinstaller pillow -q

echo.
echo Building executable...
cd program
pyinstaller --clean --noconfirm build_spec.spec

if not exist "dist\Workit\Workit.exe" (
    echo ====================================
    echo   BUILD FAILED!
    echo ====================================
    echo EXE not found. Please check error messages above.
    pause
    exit /b 1
)

cd ..

echo.
echo Checking for Inno Setup...
if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    if not exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
        echo ====================================
        echo   ERROR: Inno Setup not found!
        echo ====================================
        echo Please install Inno Setup 6 from:
        echo https://jrsoftware.org/isdl.php
        echo.
        echo After installation, run this script again.
        pause
        exit /b 1
    )
)

echo.
echo Building installer with Inno Setup...

REM 尝试两个可能的 Inno Setup 位置
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
) else (
    "C:\Program Files\Inno Setup 6\ISCC.exe" installer.iss
)

echo.
if exist "dist\Centisky-Setup-1.0.0.exe" (
    echo ====================================
    echo   BUILD SUCCESS!
    echo ====================================
    echo.
    echo Installer location:
    echo %CD%\dist\Centisky-Setup-1.0.0.exe
    echo.
    echo You can share this installer with others!
    echo They can run it to install Centisky on their computer.
    echo.
    echo Opening output folder...
    explorer "dist"
) else (
    echo ====================================
    echo   BUILD FAILED!
    echo ====================================
    echo Installer not created. Please check error messages above.
)

pause
