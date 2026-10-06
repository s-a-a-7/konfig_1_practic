@echo off
REM Тест: VFS с несколькими файлами в корне.

cd /d "%~dp0\.."

set VFS_DIR=%TEMP%\vfs_multi
if exist "%VFS_DIR%" rmdir /s /q "%VFS_DIR%"
mkdir "%VFS_DIR%"
echo alpha > "%VFS_DIR%\a.txt"
echo beta  > "%VFS_DIR%\b.txt"
echo gamma > "%VFS_DIR%\c.txt"

echo === test VFS with several files ===
python -m src.app --vfs "%VFS_DIR%" --script tests\start_script.txt