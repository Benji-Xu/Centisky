@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title Centisky - Verify Improvements

echo ====================================
echo   Centisky - Verify Improvements
echo ====================================
echo.

set "passed=0"
set "failed=0"

REM 检查 1: 唯品会开票工具中是否移除了图标设置
echo [1/5] Checking invoice processor icon removal...
findstr /M "不设置窗口图标" "program\tools\invoice_processor\main.py" >nul
if !errorlevel! equ 0 (
    echo ✓ Invoice processor: Icon removed
    set /a passed+=1
) else (
    echo ✗ Invoice processor: Icon NOT removed
    set /a failed+=1
)

REM 检查 2: launcher.py 中是否移除了图标设置
echo [2/5] Checking launcher icon removal...
findstr /M "不设置窗口图标" "program\launcher.py" >nul
if !errorlevel! equ 0 (
    echo ✓ Launcher: Icon removed
    set /a passed+=1
) else (
    echo ✗ Launcher: Icon NOT removed
    set /a failed+=1
)

REM 检查 3: README.md 中是否更新了署名
echo [3/5] Checking README signature update...
findstr /M "Benjamin" "README.md" >nul
if !errorlevel! equ 0 (
    echo ✓ README: Signature updated to Benjamin
    set /a passed+=1
) else (
    echo ✗ README: Signature NOT updated
    set /a failed+=1
)

REM 检查 4: 唯品会开票工具中是否有红冲备注改进
echo [4/5] Checking VIP invoice red flush improvement...
findstr /M "is_red_invoice" "program\tools\invoice_processor\main.py" >nul
if !errorlevel! equ 0 (
    echo ✓ VIP invoice: Red flush moved to remarks
    set /a passed+=1
) else (
    echo ✗ VIP invoice: Red flush improvement NOT found
    set /a failed+=1
)

REM 检查 5: 清理脚本是否存在
echo [5/5] Checking cleanup script...
if exist "cleanup_redundant_docs.bat" (
    echo ✓ Cleanup script exists
    set /a passed+=1
) else (
    echo ✗ Cleanup script NOT found
    set /a failed+=1
)

echo.
echo ====================================
echo   Verification Results
echo ====================================
echo.
echo Passed: %passed%/5
echo Failed: %failed%/5
echo.

if !failed! equ 0 (
    echo ✅ All improvements verified successfully!
    echo.
    echo Next steps:
    echo 1. Run: cleanup_redundant_docs.bat
    echo 2. Run: start.bat
    echo 3. Test the improvements
) else (
    echo ⚠️  Some improvements may not be applied correctly.
    echo Please check the failed items above.
)

echo.
pause
