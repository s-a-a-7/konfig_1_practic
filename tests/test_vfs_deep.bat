@echo off
REM Тест: VFS с вложенностью 3+ уровней.

cd /d "%~dp0\.."

set VFS_DIR=%TEMP%\vfs_deep
if exist "%VFS_DIR%" rmdir /s /q "%VFS_DIR%"
mkdir "%VFS_DIR%"
mkdir "%VFS_DIR%\dir1"
mkdir "%VFS_DIR%\dir1\dir2"
mkdir "%VFS_DIR%\dir1\dir2\dir3"

echo root  > "%VFS_DIR%\root.txt"
echo one   > "%VFS_DIR%\dir1\one.txt"
echo two   > "%VFS_DIR%\dir1\dir2\two.txt"
echo three > "%VFS_DIR%\dir1\dir2\dir3\three.txt"

echo === test deep VFS ===
python -m src.app --vfs "%VFS_DIR%" --script tests\start_script.txt