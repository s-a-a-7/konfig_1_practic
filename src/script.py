"""Чтение и выполнение стартового скрипта."""

import os


class ScriptError(Exception):
    """Ошибка работы со стартовым скриптом."""

def read_lines(path):
    """Читает строки скрипта, пропуская пустые.

    :raises ScriptError: если файл не существует или не читается.
    """
    if not os.path.exists(path):
        raise ScriptError(f"script not found: {path}")
    if not os.path.isfile(path):
        raise ScriptError(f"not a regular file: {path}")

    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw_lines = fh.readlines()
    except OSError as exc:
        raise ScriptError(f"cannot read script: {exc}") from exc

    return [line.rstrip("\n") for line in raw_lines if line.strip()]

def run_script(shell, path):
    """Выполняет скрипт: возвращает список (ввод, вывод).

    Ошибочные строки пропускаются — цикл не прерывается.
    """
    lines = read_lines(path)
    transcript = []
    for line in lines:
        result = shell.execute(line)
        transcript.append((line, result))
    return transcript