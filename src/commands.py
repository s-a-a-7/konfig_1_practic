"""Обработка команд эмулятора (этап 1: только заглушки)."""

from src.parser import ParseError, parse_line


class Shell:
    """Логика оболочки: разбор строки, диспетчер команд."""

    def __init__(self, vfs_name=None):
        """
        :param vfs_name: имя VFS для отображения в заголовке окна.
        """
        self.vfs_name = vfs_name
        self.should_exit = False

    def execute(self, line):
        """Выполняет одну строку, возвращает текст ответа.

        :returns: строка для отображения или None, если ответа нет.
        """
        try:
            cmd, args = parse_line(line)
        except ParseError as exc:
            return f"error: {exc}"

        if cmd is None:
            return None
        if cmd == "exit":
            self.should_exit = True
            return None

        if cmd == "ls":
            return self.cmd_ls(args)
        if cmd == "cd":
            return self.cmd_cd(args)

        return f"error: unknown command: {cmd}"

    def cmd_ls(self, args):
        """Заглушка: печатает имя команды и аргументы."""
        return self._stub("ls", args)

    def cmd_cd(self, args):
        """Заглушка: печатает имя команды и аргументы."""
        return self._stub("cd", args)
    @staticmethod
    def _stub(name, args):
        """Формирует ответ заглушки: имя команды и её аргументы."""
        if args:
            return f"{name}: args={args}"
        return f"{name}: no args"