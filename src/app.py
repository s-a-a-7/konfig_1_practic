"""Точка входа приложения."""

import sys

from src.commands import Shell
from src.config import parse_args
from src.gui import MainWindow
from src.vfs import Vfs, VfsError

def main(argv=None):
    """Создаёт окно и запускает его."""
    args = parse_args(argv)

    print(f"[DEBUG] vfs    = {args.vfs}")
    print(f"[DEBUG] script = {args.script}")

    vfs = None
    vfs_name = None
    if args.vfs:
        try:
            vfs = Vfs.from_directory(args.vfs)
            vfs_name = vfs.name
        except VfsError as exc:
            print(f"[VFS ERROR] {exc}", file=sys.stderr)
            vfs_name = None

    shell = Shell(vfs=vfs, vfs_name=vfs_name)
    window = MainWindow(shell, script_path=args.script)
    window.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())