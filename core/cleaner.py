"""Cleaning utilities for temporary and cache files."""
from __future__ import annotations

import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Iterable, Optional

from .utils import configure_logging

configure_logging()

LOGGER = logging.getLogger(__name__)


def _user_temp_dir() -> Path:
    custom = os.environ.get("TEMP") or os.environ.get("TMP")
    if custom:
        return Path(custom)
    return Path(tempfile.gettempdir())


CLEAN_TARGETS: Dict[str, Path] = {
    "User Temp": _user_temp_dir(),
    "System Temp": Path(r"C:\\Windows\\Temp"),
    "Windows Update Cache": Path(r"C:\\Windows\\SoftwareDistribution\\Download"),
    "System Logs": Path(r"C:\\Windows\\Logs"),
    "Prefetch": Path(r"C:\\Windows\\Prefetch"),
}


def _is_windows() -> bool:
    return os.name == "nt"


def clean_directory(path: Path, dry_run: bool = False) -> int:
    """Clean the provided directory and return bytes removed."""
    if not path or not path.exists():
        LOGGER.info("Skipping missing directory: %s", path)
        return 0

    removed = 0
    for root, dirs, files in os.walk(path, topdown=False):
        for file_name in files:
            file_path = Path(root) / file_name
            try:
                if dry_run:
                    removed += file_path.stat().st_size
                else:
                    removed += file_path.stat().st_size
                    file_path.unlink(missing_ok=True)
            except (PermissionError, FileNotFoundError):
                LOGGER.warning("Unable to remove file: %s", file_path)
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            try:
                if not dry_run:
                    dir_path.rmdir()
            except OSError:
                continue
    return removed


def clean_with_shell(path: Path) -> None:
    """Use Windows shell commands for faster cleanup when available."""
    if not _is_windows():
        return
    subprocess.run(f'del /f /s /q "{path}\\*" >nul 2>nul', shell=True, check=False)
    subprocess.run(f'for /d %i in ("{path}\\*") do rd /s /q "%i" >nul 2>nul', shell=True, check=False)


def clean_target(name: str, dry_run: bool = False) -> int:
    path = CLEAN_TARGETS.get(name)
    if not path:
        raise KeyError(f"Unknown clean target: {name}")
    LOGGER.info("Cleaning target %s at %s", name, path)
    if _is_windows() and not dry_run:
        clean_with_shell(path)
        return 0
    return clean_directory(path, dry_run=dry_run)


def _iter_files(path: Path) -> Iterable[Path]:
    def _on_error(error: OSError) -> None:
        LOGGER.debug("Unable to access directory during summary: %s", error)

    for root, _, files in os.walk(path, onerror=_on_error):
        for file_name in files:
            yield Path(root) / file_name


def summarize_targets(targets: Optional[Dict[str, Path]] = None) -> Dict[str, int]:
    summary: Dict[str, int] = {}
    for name, path in (targets or CLEAN_TARGETS).items():
        if not path.exists():
            summary[name] = 0
            continue
        total = 0
        for file_path in _iter_files(path):
            try:
                total += file_path.stat().st_size
            except (FileNotFoundError, PermissionError, OSError):
                LOGGER.debug("Unable to stat file: %s", file_path)
        summary[name] = total
    return summary
