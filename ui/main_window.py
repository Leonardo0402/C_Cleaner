"""Main window for the C Drive Space Manager application."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .tabs.scan_tab import ScanTab
from .tabs.clean_tab import CleanTab
from .tabs.move_tab import MoveTab
from .tabs.optimize_tab import OptimizeTab
from .tabs.insight_tab import InsightTab


class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("C盘空间管理助手")
        self.geometry("1000x600")
        self._create_widgets()

    def _create_widgets(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        self.scan_tab = ScanTab(notebook)
        self.clean_tab = CleanTab(notebook)
        self.move_tab = MoveTab(notebook)
        self.optimize_tab = OptimizeTab(notebook)
        self.insight_tab = InsightTab(notebook)

        notebook.add(self.scan_tab, text="📊 磁盘扫描")
        notebook.add(self.clean_tab, text="🧹 清理中心")
        notebook.add(self.move_tab, text="📂 目录迁移")
        notebook.add(self.optimize_tab, text="⚙️ 系统优化")
        notebook.add(self.insight_tab, text="🧠 智能分析")


def run_app() -> None:
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    run_app()
