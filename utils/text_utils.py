"""
Text utility functions for filename sanitization and role abbreviations.
"""

import re
from config import ROLE_ABBREVIATIONS


def sanitize_for_filename(text: str) -> str:
    """
    Convert text to a safe filename format.

    - Strips whitespace
    - Replaces spaces with underscores
    - Removes problematic characters

    Args:
        text: The text to sanitize

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
