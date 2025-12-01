@echo off
REM 删除不必要的修复说明文档
cd /d d:\Workit

echo 开始删除不必要的文件...

del /f "CLIPBOARD_FIX_SUMMARY.md"
del /f "FINAL_MISSING_LABELS_FIX.md"
del /f "LABEL_STATISTICS_ALERT_FIX.md"
del /f "MISSING_DETAILS_DEBUG.md"
del /f "MISSING_LABELS_EXPORT_FIX.md"
del /f "PROPELLER_COPY_FIX.md"
del /f "PROPELLER_DYNAMIC_LOADING_FIX.md"
del /f "PROPELLER_MATCHING_FIX.md"
del /f "PROPELLER_MISSING_ALERT_FIX.md"
del /f "PROPELLER_PLUS_SIGN_FIX.md"
del /f "RAZER_3D_FINAL.md"
del /f "RAZER_STYLE_GUIDE.md"
del /f "README_RAZER_UPGRADE.md"
del /f "UPGRADE_SUMMARY.md"
del /f "内嵌FFmpeg说明.md"

echo 删除完成！
pause
