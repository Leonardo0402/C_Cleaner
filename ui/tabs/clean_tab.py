"""Cleaning tab implementation."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from core import cleaner


class CleanTab(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.check_vars = {}
        for name in cleaner.CLEAN_TARGETS:
            var = tk.BooleanVar(value=False)
            check = ttk.Checkbutton(self, text=name, variable=var)
            check.pack(anchor="w", padx=20, pady=5)
            self.check_vars[name] = var

        self.status = tk.StringVar(value="请选择要清理的目标")
        ttk.Button(self, text="执行清理", command=self.execute).pack(pady=10)
        ttk.Label(self, textvariable=self.status).pack(pady=5)

    def execute(self) -> None:
        total_removed = 0
        for name, var in self.check_vars.items():
            if var.get():
                total_removed += cleaner.clean_target(name, dry_run=True)
        self.status.set(f"预计可清理 {total_removed / (1024 ** 3):.2f} GB")
