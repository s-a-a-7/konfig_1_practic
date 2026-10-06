@echo off
REM Тест: vfs-info без загруженной VFS -> error: VFS not loaded.

cd /d "%~dp0\.."

echo === test vfs-info without VFS ===
python -m src.app --script tests\start_script.txt