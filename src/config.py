"""Разбор параметров командной строки эмулятора."""

import argparse


def build_parser():
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog="shell-emulator",
        description="Эмулятор UNIX-подобной оболочки (GUI)",
    )
    parser.add_argument(
        "--vfs",
        default=None,
        help="путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script",
        default=None,
        help="путь к стартовому скрипту",
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version="shell-emulator 0.2.0",
    )
    return parser


def parse_args(argv=None):
    """Разбирает аргументы и возвращает namespace."""
    return build_parser().parse_args(argv)