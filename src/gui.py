"""Графический интерфейс эмулятора."""

import os
import sys

import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

from src.script import ScriptError, run_script


class MainWindow:
    """Главное окно приложения."""

    def __init__(self, shell, script_path=None):
        """
        :param shell: объект Shell для обработки команд.
        :param script_path: путь к стартовому скрипту (или None).
        """
        self.shell = shell
        self.script_path = script_path
        self.root = tk.Tk()
        self.root.title(self._make_title())
        self.root.geometry("700x450")

        self.output = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state=tk.DISABLED,
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=6, pady=(6, 0))

        self.entry = tk.Entry(self.root)
        self.entry.pack(fill=tk.X, padx=6, pady=6)
        self.entry.bind("<Return>", self._on_enter)

        self.entry.focus_set()

    def _append(self, text):
        """Добавляет строку в поле вывода."""
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def _on_enter(self, _event):
        """Обработчик нажатия Enter в поле ввода."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)

        self._append(f"$ {line}")

        result = self.shell.execute(line)

        if result is not None:
            self._append(result)

        if self.shell.should_exit:
            self.root.destroy()

    def _make_title(self):
        """Формирует заголовок окна с именем VFS."""
        name = self.shell.vfs_name or "none"
        return f"Shell Emulator — VFS: {name}"

    def run(self):
        """Запускает главный цикл окна."""
        if self.script_path:
            self.root.after(100, self._play_script)
        self.root.mainloop()

    def _play_script(self):
        """Проигрывает стартовый скрипт, отображая диалог."""
        if not self.script_path:
            return

        try:
            transcript = run_script(self.shell, self.script_path)
        except ScriptError as exc:
            messagebox.showerror("Script error", str(exc))
            return

        for line, result in transcript:
            self._append(f"$ {line}")
            if result is not None:
                self._append(result)
            if self.shell.should_exit:
                self.root.destroy()
                return