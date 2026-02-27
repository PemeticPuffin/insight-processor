"""
Text utility functions for filename sanitization and role abbreviations.
"""

import re
from typing import Optional
from config import ROLE_ABBREVIATIONS, ROLE_FOLDER_DEFINITIONS


def sanitize_for_filename(text: str, max_length: int = 100) -> str:
    """
    Convert text to a safe filename format.

    - Strips whitespace
    - Replaces spaces with underscores
    - Removes problematic characters
    - Truncates to max_length to avoid filesystem limits

    Args:
        text: The text to sanitize
        max_length: Maximum length of the sanitized string (default 100).
                    Set to 0 or None to disable truncation.

    Returns:
        Sanitized string safe for use in filenames
    """
    # Strip whitespace
    cleaned = text.strip()

    # Replace spaces with underscores
    cleaned = cleaned.replace(' ', '_')

    # Remove any characters that might be problematic in filenames
    # Keep alphanumeric, underscores, and hyphens
    cleaned = re.sub(r'[^\w\-]', '', cleaned)

    # Truncate to max_length if specified
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
        # Remove trailing underscores or hyphens for cleaner filenames
        cleaned = cleaned.rstrip('_-')

    return cleaned


def get_role_abbreviation(heading: str) -> str:
    """
    Get the abbreviated form of a role/heading.

    Uses role folder definitions to find the canonical short name,
    falling back to ROLE_ABBREVIATIONS for additional mappings.

    Args:
        heading: The full heading text (e.g., "Chief Audit Executive")

    Returns:
        The abbreviation (e.g., "CAE") or the original text with
        spaces replaced by underscores if no mapping exists
    """
    heading_lower = heading.strip().lower()

    # First check role folder definitions (case-insensitive)
    for create_name, _, synonyms in ROLE_FOLDER_DEFINITIONS:
        for synonym in synonyms:
            if synonym.lower() == heading_lower:
                return create_name

    # Check for exact match in role abbreviations map
    if heading in ROLE_ABBREVIATIONS:
        return ROLE_ABBREVIATIONS[heading]

    # Return sanitized version of the heading if no mapping
    return sanitize_for_filename(heading)


def get_role_full_name(role_name: str) -> Optional[str]:
    """
    Get the full display name for a role.

    Args:
        role_name: Any synonym or canonical name for the role (e.g., "CAE", "Chief Audit Executive")

    Returns:
        The full name (e.g., "Chief Audit Executive") or None if not found
    """
    role_lower = role_name.strip().lower()

    for _, full_name, synonyms in ROLE_FOLDER_DEFINITIONS:
        for synonym in synonyms:
            if synonym.lower() == role_lower:
                return full_name

    return None
