@echo off
REM Тест: ошибочные строки в скрипте пропускаются, цикл не прерывается.
REM Скрипт специально содержит неизвестную команду и незакрытую кавычку.

cd /d "%~dp0\.."
echo === test errors inside script are skipped ===

REM Создаём временный скрипт с ошибками.
(
  echo ls
  echo nosuchcommand
  echo ls "unterminated
  echo.
  echo cd dir1
) > "%TEMP%\bad_script.txt"

python -m src.app --script "%TEMP%\bad_script.txt"