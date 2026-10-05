"""Точка входа приложения."""

import os
import sys

from src.commands import Shell
from src.config import parse_args
from src.gui import MainWindow


def _vfs_name_from_path(path):
    """Извлекает имя VFS из пути (или возвращает None)."""
    if not path:
        return None
    return os.path.basename(os.path.abspath(path))


def main(argv=None):
    """Создаёт окно и запускает его."""
    args = parse_args(argv)

    """Отладочный вывод параметров"""
    print(f"[DEBUG] vfs    = {args.vfs}")
    print(f"[DEBUG] script = {args.script}")

    vfs_name = _vfs_name_from_path(args.vfs)
    shell = Shell(vfs_name=vfs_name)
    window = MainWindow(shell, script_path=args.script)
    window.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())