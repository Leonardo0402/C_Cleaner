"""Directory migration tab."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from pathlib import Path

from core import mover


class MoveTab(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.src_path = tk.StringVar()
        self.dst_path = tk.StringVar(value="D:/Migrated")

        ttk.Label(self, text="源目录").pack(anchor="w", padx=10, pady=5)
        ttk.Entry(self, textvariable=self.src_path, width=50).pack(padx=10)
        ttk.Button(self, text="选择目录", command=self._choose_src).pack(pady=5)

        ttk.Label(self, text="目标根目录").pack(anchor="w", padx=10, pady=5)
        ttk.Entry(self, textvariable=self.dst_path, width=50).pack(padx=10)

        ttk.Button(self, text="模拟迁移", command=self._simulate).pack(pady=10)

    def _choose_src(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.src_path.set(path)

    def _simulate(self) -> None:
        try:
            src = Path(self.src_path.get())
            dst_root = Path(self.dst_path.get())
            projected = mover.migrate_directory(src, dst_root, dry_run=True)
            messagebox.showinfo("预估结果", f"迁移后目录: {projected}")
        except mover.MigrationError as exc:
            messagebox.showerror("错误", str(exc))
