@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title Centisky - Build Installer with Inno Setup

echo ====================================
echo   Centisky - Build Installer
echo   Using Inno Setup 6
echo ====================================
echo.

REM 检查 Inno Setup 是否已安装
set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "!INNO_PATH!" (
    echo ERROR: Inno Setup 6 not found at !INNO_PATH!
    echo Please install Inno Setup 6 from: https://jrsoftware.org/isdl.php
    pause
    exit /b 1
)

echo [1/3] Building executable...
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

REM 安装构建工具
echo Installing build tools...
pip install pyinstaller pillow -q

REM 构建 EXE
cd program
echo Building executable with PyInstaller...
pyinstaller --clean --noconfirm build_spec.spec

if not exist "dist\Workit\Workit.exe" (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

cd ..

echo.
echo [2/3] Preparing installer files...
echo.

REM 确保输出目录存在
if not exist "dist" mkdir dist

echo [3/3] Creating installer with Inno Setup...
echo.

REM 调用 Inno Setup 编译器
"!INNO_PATH!" /O"dist" /F"Centisky-Setup-1.0.0" "installer.iss"

if errorlevel 1 (
    echo.
    echo ERROR: Inno Setup compilation failed!
    pause
    exit /b 1
)

echo.
echo ====================================
echo   BUILD SUCCESS!
echo ====================================
echo.
echo Installer created:
echo dist\Centisky-Setup-1.0.0.exe
echo.
echo Next steps:
echo 1. Test the installer on a clean system
echo 2. Create a GitHub Release
echo 3. Upload the installer to the release
echo.
echo Opening output folder...
explorer "dist"

pause
