"""Точка входа приложения (этап 1: GUI-прототип)."""

import os
import sys

from src.commands import Shell
from src.gui import MainWindow


def _get_vfs_name(argv):
    """Извлекает имя VFS из аргументов командной строки.

    Ожидает форму: --vfs <путь>. Если параметр не указан — возвращает None.
    """
    if "--vfs" in argv:
        idx = argv.index("--vfs")
        if idx + 1 < len(argv):
            path = argv[idx + 1]
            return os.path.basename(os.path.abspath(path))
    return None


def main(argv=None):
    """Создаёт окно и запускает его."""
    if argv is None:
        argv = sys.argv[1:]

    vfs_name = _get_vfs_name(argv)
    shell = Shell(vfs_name=vfs_name)
    window = MainWindow(shell)
    window.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())