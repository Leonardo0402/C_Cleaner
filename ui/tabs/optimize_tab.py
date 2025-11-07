"""System optimization tab."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from core import optimizer


class OptimizeTab(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        ttk.Label(self, text="系统优化命令").pack(anchor="w", padx=10, pady=5)

        self.listbox = tk.Listbox(self)
        for command in optimizer.list_commands():
            self.listbox.insert(tk.END, command)
        self.listbox.pack(expand=True, fill="both", padx=10, pady=5)

        ttk.Button(self, text="执行", command=self._run_command).pack(pady=10)

    def _run_command(self) -> None:
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("提示", "请选择需要执行的命令")
            return
        name = self.listbox.get(selection[0])
        optimizer.run_command(name, dry_run=True)
        messagebox.showinfo("提示", f"命令 {name} 已模拟执行")
