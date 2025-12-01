@echo off
echo ====================================
echo   Clearing Windows Icon Cache
echo ====================================
echo.

echo Stopping Windows Explorer...
taskkill /f /im explorer.exe

echo.
echo Deleting icon cache files...
cd /d %userprofile%\AppData\Local
attrib -h IconCache.db
del IconCache.db /a
del IconCache.db /f /q
del /f /s /q /a %userprofile%\AppData\Local\Microsoft\Windows\Explorer\iconcache*

echo.
echo Restarting Windows Explorer...
start explorer.exe

echo.
echo ====================================
echo   Icon cache cleared!
echo ====================================
echo Please restart your computer if icons still appear incorrect.
echo.
pause



