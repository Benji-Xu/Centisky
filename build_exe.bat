@echo off
chcp 65001 >nul
title Centisky - Build Executable
echo ====================================
echo   Centisky - Building Executable
echo   Developed by @Benji-Xu with Windsurf
echo ====================================
echo.
echo 提示：如果你想生成安装程序而不是单独的 EXE，
echo 请运行 build_installer.bat 脚本。
echo.
pause

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

echo.
if exist "dist\Workit\Workit.exe" (
    echo ====================================
    echo   BUILD SUCCESS!
    echo ====================================
    echo.
    echo Executable location:
    echo %CD%\dist\Workit\Workit.exe
    echo.
    echo You can share the entire 'dist\Workit' folder
    echo Others can run it directly without Python!
    echo.
    echo Opening output folder...
    explorer "dist\Workit"
) else (
    echo ====================================
    echo   BUILD FAILED!
    echo ====================================
    echo Please check error messages above
)

pause

