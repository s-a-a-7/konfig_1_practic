@echo off
REM Тест: минимальная VFS - одна папка с одним файлом.

cd /d "%~dp0\.."

set VFS_DIR=%TEMP%\vfs_min
if exist "%VFS_DIR%" rmdir /s /q "%VFS_DIR%"
mkdir "%VFS_DIR%"
echo hello > "%VFS_DIR%\a.txt"

echo === test minimal VFS ===
python -m src.app --vfs "%VFS_DIR%" --script tests\start_script.txt