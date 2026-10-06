@echo off
REM Тест этапа 5: все основные команды.

cd /d "%~dp0\.."

set VFS_DIR=%TEMP%\vfs_stage5
if exist "%VFS_DIR%" rmdir /s /q "%VFS_DIR%"
mkdir "%VFS_DIR%"
mkdir "%VFS_DIR%\dir1"
mkdir "%VFS_DIR%\dir1\dir2"

echo alpha > "%VFS_DIR%\a.txt"
echo beta  > "%VFS_DIR%\b.txt"
echo one   > "%VFS_DIR%\dir1\one.txt"
echo two   > "%VFS_DIR%\dir1\dir2\two.txt"

(
  echo line1
  echo line2
  echo line3
  echo line4
  echo line5
) > "%VFS_DIR%\multi.txt"

echo === stage 5: all basic commands ===
python -m src.app --vfs "%VFS_DIR%" --script tests\start_script.txt