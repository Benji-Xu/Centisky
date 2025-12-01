@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title Centisky - Setup Checker

echo ====================================
echo   Centisky - Setup Checker
echo ====================================
echo.

set "all_ok=1"

REM 检查 Python
echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    echo    Please install Python from: https://www.python.org
    set "all_ok=0"
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set "python_version=%%i"
    echo ✓ Python !python_version! found
)

REM 检查 PyInstaller
echo.
echo [2/4] Checking PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ⚠ PyInstaller not installed
    echo    Installing...
    pip install pyinstaller -q
    if errorlevel 1 (
        echo ❌ Failed to install PyInstaller
        set "all_ok=0"
    ) else (
        echo ✓ PyInstaller installed
    )
) else (
    echo ✓ PyInstaller found
)

REM 检查 Inno Setup
echo.
echo [3/4] Checking Inno Setup 6...
set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if exist "!INNO_PATH!" (
    echo ✓ Inno Setup 6 found
) else (
    echo ❌ Inno Setup 6 not found at:
    echo    !INNO_PATH!
    echo.
    echo    Download from: https://jrsoftware.org/isdl.php
    echo    Install to default location
    set "all_ok=0"
)

REM 检查必要文件
echo.
echo [4/4] Checking required files...
set "files_ok=1"

if exist "version.txt" (
    echo ✓ version.txt found
) else (
    echo ❌ version.txt not found
    set "files_ok=0"
)

if exist "installer.iss" (
    echo ✓ installer.iss found
) else (
    echo ❌ installer.iss not found
    set "files_ok=0"
)

if exist "program\launcher.py" (
    echo ✓ program/launcher.py found
) else (
    echo ❌ program/launcher.py not found
    set "files_ok=0"
)

if exist "program\update_checker.py" (
    echo ✓ program/update_checker.py found
) else (
    echo ❌ program/update_checker.py not found
    set "files_ok=0"
)

if !files_ok! equ 0 (
    set "all_ok=0"
)

REM 总结
echo.
echo ====================================
if !all_ok! equ 1 (
    echo   ✓ All checks passed!
    echo ====================================
    echo.
    echo You can now run:
    echo   build_installer_auto.bat
    echo.
) else (
    echo   ❌ Some checks failed
    echo ====================================
    echo.
    echo Please fix the issues above and try again.
    echo.
)

pause
