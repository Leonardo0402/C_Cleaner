"""Directory migration utilities."""
from __future__ import annotations

import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Tuple

from .utils import configure_logging

configure_logging()
LOGGER = logging.getLogger(__name__)


class MigrationError(RuntimeError):
    """Raised when a migration operation fails."""


def validate_paths(src: Path, dst_root: Path) -> Tuple[Path, Path]:
    if not src.exists():
        raise MigrationError(f"Source path does not exist: {src}")
    if not src.is_dir():
        raise MigrationError(f"Source path must be a directory: {src}")
    dst_root.mkdir(parents=True, exist_ok=True)
    dst = dst_root / src.name
    return src.resolve(), dst.resolve()


def _is_windows() -> bool:
    return os.name == "nt"


def _create_junction(src: Path, dst: Path) -> None:
    if not _is_windows():
        return
    subprocess.run(["cmd", "/c", "rmdir", str(src)], check=False)
    subprocess.run(["cmd", "/c", "mklink", "/J", str(src), str(dst)], check=True)


def migrate_directory(src: Path, dst_root: Path, dry_run: bool = False) -> Path:
    """Move the source directory to a new root and create a junction."""
    src, dst = validate_paths(src, dst_root)
    LOGGER.info("Migrating %s to %s", src, dst)
    if dry_run:
        return dst
    if dst.exists():
        raise MigrationError(f"Destination already exists: {dst}")
    shutil.move(str(src), str(dst))
    if _is_windows():
        _create_junction(src, dst)
    return dst
