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

    def resolve(self, cwd, path):
        """Преобразует путь относительно cwd в абсолютный путь внутри VFS."""
        if path.startswith("/"):
            parts = [p for p in path.split("/") if p]
        else:
            parts = [p for p in (cwd + "/" + path).split("/") if p]

        result = []
        for part in parts:
            if part == ".":
                continue
            if part == "..":
                if result:
                    result.pop()
                continue
            result.append(part)
        return "/" + "/".join(result)

    def list_dir(self, cwd, path):
        """Возвращает отсортированный список имён в директории."""
        target = self.resolve(cwd, path).lstrip("/")
        if target:
            prefix = target + "/"
        else:
            prefix = ""
        names = set()
        for key in self.data:
            if key.startswith(prefix):
                rest = key[len(prefix):]
                if "/" in rest:
                    names.add(rest.split("/", 1)[0] + "/")
                else:
                    names.add(rest)
        return sorted(names)

    def is_file(self, cwd, path):
        """Проверяет, что путь — обычный файл в VFS."""
        target = self.resolve(cwd, path).lstrip("/")
        return bool(target) and target in self.data

    def is_dir(self, cwd, path):
        """Проверяет, что путь — директория в VFS."""
        target = self.resolve(cwd, path).lstrip("/")
        if not target:
            return True
        prefix = target + "/"
        return any(key.startswith(prefix) for key in self.data)

    def exists(self, cwd, path):
        """Проверяет, что путь существует (как файл или как директория)."""
        return self.is_file(cwd, path) or self.is_dir(cwd, path)

    def read_file(self, cwd, path):
        """Читает файл, возвращает список строк."""
        target = self.resolve(cwd, path).lstrip("/")
        if target not in self.data:
            raise VfsError(f"no such file: {path}")
        return self.data[target].splitlines()

    def remove(self, cwd, path):
        """Удаляет файл или директорию (рекурсивно) из VFS."""
        target = self.resolve(cwd, path).lstrip("/")
        if not target:
            raise VfsError("cannot remove root")
        prefix = target + "/"
        keys = [k for k in self.data if k == target or k.startswith(prefix)]
        if not keys:
            raise VfsError(f"no such file or directory: {path}")
        for k in keys:
            del self.data[k]

    def move(self, cwd, src, dst):
        """Перемещает файл или директорию внутри VFS."""
        src_abs = self.resolve(cwd, src).lstrip("/")
        dst_abs = self.resolve(cwd, dst).lstrip("/")
        if not src_abs:
            raise VfsError("cannot move root")
        if not dst_abs:
            raise VfsError("cannot move to root")

        prefix = src_abs + "/"
        keys = [k for k in self.data if k == src_abs or k.startswith(prefix)]
        if not keys:
            raise VfsError(f"no such file or directory: {src}")

        for k in keys:
            suffix = k[len(src_abs):]
            new_key = dst_abs + suffix
            self.data[new_key] = self.data.pop(k)