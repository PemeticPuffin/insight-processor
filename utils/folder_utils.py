"""
Folder utility functions for creation and matching.
"""

import re
from pathlib import Path
from typing import Optional, Tuple, List

from config import ROLE_FOLDER_DEFINITIONS


def get_role_folder_info(role_name: str) -> Optional[Tuple[str, List[str]]]:
    """
    Get folder creation name and search synonyms for a role.

    Args:
        role_name: The role name from input (e.g., "Tech CMO", "R&D")

    Returns:
        Tuple of (create_name, search_names) if role is known, None otherwise.
        - create_name: the canonical folder name to create
        - search_names: all folder name variations to search for
    """
    role_lower = role_name.strip().lower()

    for create_name, _, synonyms in ROLE_FOLDER_DEFINITIONS:
        for synonym in synonyms:
            if synonym.lower() == role_lower:
                return (create_name, synonyms)

    return None


def sanitize_folder_name(name: str) -> str:
    """
    Sanitize a name for use as a folder name (no underscores).

    - Strips whitespace
    - Removes problematic filesystem characters
    - Preserves spaces (unlike filename sanitization)

    Args:
        name: The name to sanitize

    Returns:
        Sanitized string safe for use as folder name
    """
    # Strip whitespace
    cleaned = name.strip()

    # Remove characters that are problematic in folder names
    # Keep alphanumeric, spaces, hyphens, and some punctuation
    # Remove: / \ : * ? " < > |
    cleaned = re.sub(r'[/\\:*?"<>|]', '', cleaned)

    # Collapse multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)

    return cleaned.strip()


def ensure_subfolder_exists(parent: Path, name: str) -> Tuple[Path, bool]:
    """
    Ensure a subfolder exists, creating it only if missing.

    Uses role mapping to determine the correct folder name:
    - For known roles, uses the canonical folder name
    - For unknown roles, sanitizes the name (no underscores)

    Also searches for existing folders using role synonyms before creating.

    Args:
        parent: Parent directory path
        name: Name of the subfolder (role name from input)

    Returns:
        Tuple of (path to subfolder, True if created / False if already existed)
    """
    # Check if this is a known role
    role_info = get_role_folder_info(name)

    if role_info:
        create_name, search_names = role_info

        # First, try to find an existing folder matching any synonym
        for search_name in search_names:
            candidate = parent / search_name
            if candidate.exists() and candidate.is_dir():
                return candidate, False

            # Also try case-insensitive match
            for existing in parent.iterdir():
                if existing.is_dir() and existing.name.lower() == search_name.lower():
                    return existing, False

        # No existing folder found, create with canonical name
        subfolder = parent / create_name
        subfolder.mkdir(parents=True, exist_ok=True)
        return subfolder, True

    else:
        # Unknown role - sanitize without underscores
        safe_name = sanitize_folder_name(name)
        subfolder = parent / safe_name

        if subfolder.exists():
            return subfolder, False

        subfolder.mkdir(parents=True, exist_ok=True)
        return subfolder, True


def find_matching_subfolder(parent: Path, name: str) -> Optional[Path]:
    """
    Find a subfolder that matches the given name.

    Uses role mapping for known roles to check all synonyms.

    Matching priority for known roles:
    1. Exact match on any synonym
    2. Case-insensitive match on any synonym

    Matching priority for unknown roles:
    1. Exact match
    2. Case-insensitive match
    3. Sanitized name match

    Args:
        parent: Parent directory to search in
        name: Name to match (role name from input)

    Returns:
        Path to the matching subfolder, or None if not found
    """
    if not parent.exists() or not parent.is_dir():
        return None

    # Check if this is a known role
    role_info = get_role_folder_info(name)

    if role_info:
        _, search_names = role_info

        # Try exact match on each synonym
        for search_name in search_names:
            exact_match = parent / search_name
            if exact_match.exists() and exact_match.is_dir():
                return exact_match

        # Try case-insensitive match on each synonym
        search_names_lower = [s.lower() for s in search_names]
        for subfolder in parent.iterdir():
            if subfolder.is_dir():
                folder_lower = subfolder.name.lower()
                if folder_lower in search_names_lower:
                    return subfolder

        return None

    else:
        # Unknown role - use original matching logic

        # First try exact match
        exact_match = parent / name
        if exact_match.exists() and exact_match.is_dir():
            return exact_match

        # Try sanitized name match
        sanitized_name = sanitize_folder_name(name)
        if sanitized_name != name:
            sanitized_match = parent / sanitized_name
            if sanitized_match.exists() and sanitized_match.is_dir():
                return sanitized_match

        # Try case-insensitive match
        name_lower = name.lower()
        sanitized_lower = sanitized_name.lower()
        for subfolder in parent.iterdir():
            if subfolder.is_dir():
                folder_lower = subfolder.name.lower()
                if folder_lower == name_lower or folder_lower == sanitized_lower:
                    return subfolder

        return None
