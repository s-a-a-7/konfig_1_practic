"""Графический интерфейс эмулятора."""

import tkinter as tk
from tkinter import scrolledtext

class MainWindow:
    """Главное окно приложения."""

    def __init__(self, shell):
        """
        :param shell: объект Shell для обработки команд.
        """
        self.shell = shell
        self.root = tk.Tk()
        self.root.title(f"Shell Emulator — VFS: {shell.vfs_name or 'none'}")
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

    def run(self):
        """Запускает главный цикл окна."""
        self.root.mainloop()