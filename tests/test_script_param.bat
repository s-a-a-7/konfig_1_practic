@echo off
REM Тест: только параметр --script (без VFS).
REM Окно должно открыться с заголовком "VFS: none",
REM автоматически проиграть скрипт и закрыться по exit.

echo === test --script only (no vfs) ===
python -m src.app --script tests\start_script.txt