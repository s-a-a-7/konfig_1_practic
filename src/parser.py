import shlex

class ParseError(Exception):
    """Ошибка разбора командной строки."""

def parse_line(line):
    """Разбирает строку команды на имя и аргументы.

    :raises ParseError: если кавычки не сбалансированы.
    """
    try:
        tokens = shlex.split(line)
    except ValueError as exc:
        raise ParseError(str(exc)) from exc

    if not tokens:
        return None, []

    return tokens[0], tokens[1:]