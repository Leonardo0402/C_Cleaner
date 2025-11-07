"""Utility helpers for C Drive Space Manager."""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict

LOG_FILE = Path(__file__).resolve().parents[1] / "logs" / "actions.log"
SETTINGS_FILE = Path(__file__).resolve().parents[1] / "configs" / "settings.json"


def ensure_environment() -> None:
    """Ensure required directories and files exist."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not SETTINGS_FILE.exists():
        SETTINGS_FILE.write_text(json.dumps({}, indent=2), encoding="utf-8")


def configure_logging() -> None:
    """Configure application wide logging."""
    ensure_environment()
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def load_settings() -> Dict[str, Any]:
    ensure_environment()
    try:
        return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_settings(settings: Dict[str, Any]) -> None:
    ensure_environment()
    SETTINGS_FILE.write_text(json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8")


def is_admin() -> bool:
    """Return True if running with administrative privileges."""
    if os.name != "nt":
        return os.geteuid() == 0 if hasattr(os, "geteuid") else True
    try:
        import ctypes

        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False
