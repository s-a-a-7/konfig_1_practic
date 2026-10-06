"""Обработка команд эмулятора"""

from src.parser import ParseError, parse_line
from src.vfs import VfsError

class Shell:
    """Логика оболочки: разбор строки, диспетчер команд."""

    _VFS_COMMANDS = frozenset({"ls", "cd", "tac", "tail", "rm", "mv"})

    def __init__(self, vfs=None, vfs_name=None):
        """
        :param vfs: объект Vfs (или None, если VFS не загружена).
        :param vfs_name: имя VFS для отображения в заголовке окна.
        """
        self.vfs = vfs
        self.vfs_name = vfs_name
        self.cwd = "/"
        self.should_exit = False

    def execute(self, line):
        """Выполняет одну строку, возвращает текст ответа."""
        try:
            cmd, args = parse_line(line)
        except ParseError as exc:
            return f"error: {exc}"

        if cmd is None:
            return None
        if cmd == "exit":
            self.should_exit = True
            return None

        if cmd == "vfs-info":
            return self.cmd_vfs_info(args)
        if cmd in self._VFS_COMMANDS and self.vfs is None:
            return "error: VFS not loaded"

        if cmd == "ls":
            return self.cmd_ls(args)
        if cmd == "cd":
            return self.cmd_cd(args)
        if cmd == "tac":
            return self.cmd_tac(args)
        if cmd == "tail":
            return self.cmd_tail(args)
        if cmd == "rm":
            return self.cmd_rm(args)
        if cmd == "mv":
            return self.cmd_mv(args)

        return f"error: unknown command: {cmd}"

    def cmd_vfs_info(self, args):
        """Служебная команда: информация о загруженной VFS."""
        if self.vfs is None:
            return "error: VFS not loaded"
        return self.vfs.info()

    def cmd_ls(self, args):
        """Показывает содержимое директории."""
        path = args[0] if args else "."
        if not self.vfs.exists(self.cwd, path):
            return f"error: no such file or directory: {path}"
        if not self.vfs.is_dir(self.cwd, path):
            return f"error: not a directory: {path}"
        names = self.vfs.list_dir(self.cwd, path)
        return "\n".join(names) if names else ""

    def cmd_cd(self, args):
        """Переходит в другую директорию."""
        if not args:
            self.cwd = "/"
            return None
        path = args[0]
        if not self.vfs.exists(self.cwd, path):
            return f"error: no such file or directory: {path}"
        if not self.vfs.is_dir(self.cwd, path):
            return f"error: not a directory: {path}"
        self.cwd = self.vfs.resolve(self.cwd, path)
        return None

    def cmd_tac(self, args):
        """Выводит содержимое файла в обратном порядке строк."""
        if not args:
            return "error: tac: missing operand"
        path = args[0]
        if not self.vfs.exists(self.cwd, path):
            return f"error: no such file or directory: {path}"
        if not self.vfs.is_file(self.cwd, path):
            return f"error: is a directory: {path}"
        try:
            lines = self.vfs.read_file(self.cwd, path)
        except VfsError as exc:
            return f"error: {exc}"
        return "\n".join(reversed(lines))

    def cmd_tail(self, args):
        """Выводит последние N строк файла (по умолчанию 10)."""
        n = 10
        files = []
        i = 0
        while i < len(args):
            if args[i] == "-n" and i + 1 < len(args):
                try:
                    n = int(args[i + 1])
                except ValueError:
                    return f"error: invalid number: {args[i + 1]}"
                i += 2
            else:
                files.append(args[i])
                i += 1

        if not files:
            return "error: tail: missing operand"

        out = []
        for name in files:
            if not self.vfs.exists(self.cwd, name):
                out.append(f"error: no such file or directory: {name}")
                continue
            if not self.vfs.is_file(self.cwd, name):
                out.append(f"error: is a directory: {name}")
                continue
            try:
                lines = self.vfs.read_file(self.cwd, name)
            except VfsError as exc:
                out.append(f"error: {exc}")
                continue
            out.extend(lines[-n:] if n > 0 else [])
        return "\n".join(out)

    def cmd_rm(self, args):
        """Удаляет файлы и/или директории из VFS."""
        if not args:
            return "error: rm: missing operand"
        out = []
        for path in args:
            try:
                self.vfs.remove(self.cwd, path)
            except VfsError as exc:
                out.append(f"error: {exc}")
        return "\n".join(out) if out else None

    def cmd_mv(self, args):
        """Перемещает или переименовывает файл/директорию."""
        if len(args) != 2:
            return "error: mv: usage: mv SRC DST"
        try:
            self.vfs.move(self.cwd, args[0], args[1])
        except VfsError as exc:
            return f"error: {exc}"
        return None