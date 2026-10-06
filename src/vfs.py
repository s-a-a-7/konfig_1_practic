"""Виртуальная файловая система в памяти."""

import hashlib
import json
import os

class VfsError(Exception):
    """Ошибка загрузки/работы VFS."""

class Vfs:
    """Дерево файлов и папок, загружаемое из директории на диске."""

    def __init__(self, name, data):
        """
        :param name: имя VFS
        :param data: словарь {путь: содержимое}
        """
        self.name = name
        self.data = data

    @property
    def sha256(self):
        """SHA-256 от сериализованных данных VFS."""
        raw = json.dumps(
            self.data, sort_keys=True, ensure_ascii=False,
        ).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    @classmethod
    def from_directory(cls, path):
        """Загружает VFS из директории на диске.

        :raises VfsError: если путь не существует или не является директорией.
        """
        if not os.path.exists(path):
            raise VfsError(f"VFS path not found: {path}")
        if not os.path.isdir(path):
            raise VfsError(f"VFS path is not a directory: {path}")

        name = os.path.basename(os.path.abspath(path))
        data = {}
        for root, _dirs, files in os.walk(path):
            rel_root = os.path.relpath(root, path)
            if rel_root == ".":
                rel_root = ""
            for fname in files:
                full = os.path.join(root, fname)
                rel = os.path.join(rel_root, fname).replace(os.sep, "/")
                try:
                    with open(full, "r", encoding="utf-8-sig") as fh:
                        data[rel] = fh.read()
                except (OSError, UnicodeDecodeError) as exc:
                    raise VfsError(f"cannot read {full}: {exc}") from exc
        return cls(name, data)

    def info(self):
        """Служебная информация о VFS."""
        return f"name: {self.name}\nsha256: {self.sha256}"