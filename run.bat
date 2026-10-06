@echo off
REM Запуск эмулятора на Windows.
REM Все аргументы пробрасываются в python -m src.app.
REM Примеры:
REM   run.bat
REM   run.bat --vfs C:\temp\my_vfs
REM   run.bat --vfs C:\temp\my_vfs --script tests\start_script.txt

cd /d "%~dp0"
python -m src.app %*