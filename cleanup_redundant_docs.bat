@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title Centisky - Cleanup Redundant Documentation

echo ====================================
echo   Centisky - Cleanup Redundant Docs
echo ====================================
echo.

set "deleted_count=0"

REM 删除冗余文档
for %%F in (
    "FFmpeg安装指南.md"
    "FOLDER_RENAME_GUIDE.md"
    "INSTALLER_AND_UPDATE_PLAN.md"
    "INSTALLER_IMPLEMENTATION_SUMMARY.md"
    "INSTALLER_USAGE_GUIDE.md"
    "QUICK_START_INSTALLER.md"
    "内嵌FFmpeg说明.md"
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
echo Deleted %deleted_count% redundant documentation files
echo.
echo Remaining documentation:
echo   - README.md
echo   - COMPLETION_REPORT.md
echo   - FINAL_SUMMARY.md
echo   - GITHUB_RELEASE_GUIDE.md
echo   - IMPLEMENTATION_CHECKLIST.md
echo   - INDEX.md
echo   - INSTALLER_QUICK_START.md
echo   - INSTALLER_SETUP_COMPLETE.md
echo   - README_INSTALLER.md
echo   - SETUP_SUMMARY.md
echo.

pause
