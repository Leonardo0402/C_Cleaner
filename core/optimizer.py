"""System optimization utilities."""
from __future__ import annotations

import logging
import subprocess
from typing import List

from .utils import configure_logging

configure_logging()
LOGGER = logging.getLogger(__name__)


class OptimizationCommand:
    def __init__(self, name: str, command: List[str]):
        self.name = name
        self.command = command

    def run(self, dry_run: bool = False) -> int:
        LOGGER.info("Running optimization command: %s", self.name)
        if dry_run:
            return 0
        result = subprocess.run(self.command, shell=False, check=False)
        return result.returncode


COMMANDS = {
    "Disable Hibernation": OptimizationCommand("Disable Hibernation", ["powercfg", "-h", "off"]),
    "Move TEMP to D": OptimizationCommand("Move TEMP to D", ["setx", "TEMP", "D:\\Temp", "/M"]),
    "Delete Restore Points": OptimizationCommand(
        "Delete Restore Points", ["vssadmin", "delete", "shadows", "/all", "/quiet"]
    ),
}


def run_command(name: str, dry_run: bool = False) -> int:
    command = COMMANDS.get(name)
    if not command:
        raise KeyError(f"Unknown optimization command: {name}")
    return command.run(dry_run=dry_run)


def list_commands() -> List[str]:
    return list(COMMANDS.keys())
