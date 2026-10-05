@echo off
REM Тест: оба параметра --vfs и --script.
REM Заголовок "VFS: some_vfs", автоматический проигрыш скрипта.

cd /d "%~dp0\.."
echo === test --vfs and --script together ===
python -m src.app --vfs C:\temp\some_vfs --script tests\demo_script.txt