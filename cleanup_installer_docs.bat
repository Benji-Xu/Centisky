@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title Centisky - Cleanup Installer Documentation

echo ====================================
echo   Centisky - Cleanup Installer Docs
echo ====================================
echo.

set "deleted_count=0"

REM 删除冗余的安装程序文档
echo Deleting redundant installer documentation...
echo.

for %%F in (
    "INSTALLER_AND_UPDATE_PLAN.md"
    "INSTALLER_IMPLEMENTATION_SUMMARY.md"
    "INSTALLER_USAGE_GUIDE.md"
    "QUICK_START_INSTALLER.md"
) do (
    if exist "%%F" (
        echo Deleting: %%F
        del "%%F"
        set /a deleted_count+=1
    )
)

echo.
echo ====================================
echo   Cleanup Complete
echo ====================================
echo.
echo Deleted %deleted_count% redundant installer documentation files
echo.
echo Remaining installer documentation:
echo   - INSTALLER_QUICK_START.md (快速开始)
echo   - INSTALLER_SETUP_COMPLETE.md (详细设置)
echo   - README_INSTALLER.md (完整说明)
echo   - BUILD_INSTALLER_GUIDE.md (打包指南)
echo   - GITHUB_RELEASE_GUIDE.md (发布指南)
echo.
echo Other important files:
echo   - QUICK_BUILD_CHECKLIST.txt (打包检查清单)
echo   - QUICK_REFERENCE.txt (快速参考)
echo   - INDEX.md (文档索引)
echo.

pause
