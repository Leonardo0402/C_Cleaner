"""Disk scanning utilities for the C Drive Space Manager."""
from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union

try:  # pragma: no cover - optional dependency
    import psutil  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback path
    psutil = None  # type: ignore


@dataclass
class DirectoryStat:
    path: Path
    size: int
    children: List["DirectoryStat"]

    def to_dict(self) -> Dict[str, object]:
        return {
            "path": str(self.path),
            "size": self.size,
            "children": [child.to_dict() for child in self.children],
        }


def _iter_child_paths(path: Path) -> Iterable[Path]:
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                yield Path(entry.path)
    except (PermissionError, FileNotFoundError, NotADirectoryError):
        return


def _safe_file_size(path: Path) -> int:
    try:
        return path.stat(follow_symlinks=False).st_size
    except (PermissionError, FileNotFoundError, OSError):
        return 0


def _is_directory(path: Path) -> bool:
    try:
        return path.is_dir()
    except OSError:
        return False


def scan_directory(path: Path, depth: int = 1) -> DirectoryStat:
    """Scan a directory and return recursive size information."""
    total = 0
    children: List[DirectoryStat] = []

    if depth <= 0:
        for child in _iter_child_paths(path):
            total += _safe_file_size(child)
        return DirectoryStat(path=path, size=total, children=children)

    for child in _iter_child_paths(path):
        if child.is_symlink():
            total += _safe_file_size(child)
            continue
        if _is_directory(child):
            child_stat = scan_directory(child, depth - 1)
            total += child_stat.size
            children.append(child_stat)
        else:
            total += _safe_file_size(child)
    return DirectoryStat(path=path, size=total, children=children)


def _resolve_root(drive: Optional[Union[str, os.PathLike[str]]]) -> Path:
    if drive is None:
        candidate = Path("C:/") if os.name == "nt" else Path(os.sep)
    else:
        candidate = Path(drive)

    if candidate.exists():
        return candidate

    anchor = candidate.anchor
    if anchor:
        anchor_path = Path(anchor)
        if anchor_path.exists():
            return anchor_path

    return Path(os.sep)


def scan_drive(
    drive: Optional[Union[str, os.PathLike[str]]] = None, depth: int = 1
) -> Dict[str, object]:
    """Scan the provided drive and return a mapping suitable for UI consumption."""
    root = _resolve_root(drive)
    stat = scan_directory(root, depth=depth)
    usage_total, usage_used, usage_free, usage_percent = _disk_usage(root)
    return {
        "root": stat.to_dict(),
        "total": usage_total,
        "used": usage_used,
        "free": usage_free,
        "percent": usage_percent,
    }


def _disk_usage(path: Path) -> tuple[int, int, int, float]:
    if psutil is not None:
        usage = psutil.disk_usage(str(path))  # type: ignore[arg-type]
        return usage.total, usage.used, usage.free, usage.percent  # type: ignore[attr-defined]

    usage = shutil.disk_usage(str(path))
    percent = (usage.used / usage.total * 100) if usage.total else 0.0
    return usage.total, usage.used, usage.free, percent
