"""
Text utility functions for filename sanitization and role abbreviations.
"""

import re
from config import ROLE_ABBREVIATIONS


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

    Args:
        heading: The full heading text (e.g., "Chief Audit Executive")

    Returns:
        The abbreviation (e.g., "CAE") or the original text with
        spaces replaced by underscores if no mapping exists
    """
    # Check for exact match in role map
    if heading in ROLE_ABBREVIATIONS:
        return ROLE_ABBREVIATIONS[heading]

    # Return sanitized version of the heading if no mapping
    return sanitize_for_filename(heading)
