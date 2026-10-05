@echo off
REM Тест: только параметр --vfs (интерактивный режим).
REM Окно должно открыться с заголовком "VFS: some_vfs".
REM Закрыть окно можно командой exit или крестиком.

echo === test --vfs only (interactive mode) ===
python -m src.app --vfs C:\temp\some_vfs