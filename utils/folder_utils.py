"""
Folder utility functions for creation and matching.
"""

from pathlib import Path
from typing import Optional


def ensure_subfolder_exists(parent: Path, name: str) -> Path:
    """
    Ensure a subfolder exists, creating it if necessary.

    Args:
        parent: Parent directory path
        name: Name of the subfolder

    Returns:
        Path to the subfolder
    """
    subfolder = parent / name
    subfolder.mkdir(parents=True, exist_ok=True)
    return subfolder


def find_matching_subfolder(parent: Path, name: str) -> Optional[Path]:
    """
    Find a subfolder that matches the given name (case-insensitive).

    Args:
        parent: Parent directory to search in
        name: Name to match

    Returns:
        Path to the matching subfolder, or None if not found
    """
    if not parent.exists() or not parent.is_dir():
        return None

    # First try exact match
    exact_match = parent / name
    if exact_match.exists() and exact_match.is_dir():
        return exact_match

    # Try case-insensitive match
    name_lower = name.lower()
    for subfolder in parent.iterdir():
        if subfolder.is_dir() and subfolder.name.lower() == name_lower:
            return subfolder

    return None
