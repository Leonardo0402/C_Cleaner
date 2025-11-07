"""Insight tab implementation."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from core import analyzer, cleaner


class InsightTab(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        ttk.Button(self, text="生成推荐", command=self._generate).pack(pady=10)
        self.tree = ttk.Treeview(self, columns=("path", "size", "suggestion"), show="headings")
        self.tree.heading("path", text="目录")
        self.tree.heading("size", text="大小")
        self.tree.heading("suggestion", text="建议")
        self.tree.pack(expand=True, fill="both")

    def _generate(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        flat = cleaner.summarize_targets()
        insights = analyzer.generate_insights(flat)
        for insight in insights:
            self.tree.insert("", "end", values=(insight["path"], insight["size"], insight["suggestion"]))
