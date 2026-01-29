"""
Folder utility functions for creation and matching.
"""

from pathlib import Path
from typing import Optional, Tuple

from utils.text_utils import sanitize_for_filename


def ensure_subfolder_exists(parent: Path, name: str) -> Tuple[Path, bool]:
    """
    Ensure a subfolder exists, creating it only if missing.

    The folder name is sanitized to remove problematic characters.

    Args:
        parent: Parent directory path
        name: Name of the subfolder (will be sanitized)

    Returns:
        Tuple of (path to subfolder, True if created / False if already existed)
    """
    # Sanitize folder name (no length truncation for folders)
    safe_name = sanitize_for_filename(name, max_length=0)
    subfolder = parent / safe_name

    if subfolder.exists():
        return subfolder, False

    subfolder.mkdir(parents=True, exist_ok=True)
    return subfolder, True


def find_matching_subfolder(parent: Path, name: str) -> Optional[Path]:
    """
    Find a subfolder that matches the given name.

    Matching priority:
    1. Exact match
    2. Case-insensitive match
    3. Sanitized name match (for folders created via ensure_subfolder_exists)

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

    # Try sanitized name match (for folders created via ensure_subfolder_exists)
    sanitized_name = sanitize_for_filename(name, max_length=0)
    if sanitized_name != name:
        sanitized_match = parent / sanitized_name
        if sanitized_match.exists() and sanitized_match.is_dir():
            return sanitized_match

    # Try case-insensitive match on both original and sanitized names
    name_lower = name.lower()
    sanitized_lower = sanitized_name.lower()
    for subfolder in parent.iterdir():
        if subfolder.is_dir():
            folder_lower = subfolder.name.lower()
            if folder_lower == name_lower or folder_lower == sanitized_lower:
                return subfolder

    return None
