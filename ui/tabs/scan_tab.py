"""Scan tab implementation."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from core import scanner


class ScanTab(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.tree = ttk.Treeview(self, columns=("size",), show="tree headings")
        self.tree.heading("#0", text="目录")
        self.tree.heading("size", text="大小")
        self.tree.pack(expand=True, fill="both")

        button = ttk.Button(self, text="开始扫描", command=self.refresh)
        button.pack(pady=10)

    def refresh(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = scanner.scan_drive()
        self._populate_tree("", data["root"])

    def _populate_tree(self, parent: str, node: dict) -> None:
        size_gb = node["size"] / (1024 ** 3)
        item = self.tree.insert(parent, "end", text=node["path"], values=(f"{size_gb:.2f} GB",))
        for child in node.get("children", []):
            self._populate_tree(item, child)
