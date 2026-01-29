"""
Utility modules for Insight Processor.
"""

from .date_utils import get_two_mondays_from_now, format_date_for_filename
from .file_utils import backup_file, find_word_files, is_temp_file, validate_docx
from .folder_utils import ensure_subfolder_exists, find_matching_subfolder
from .text_utils import sanitize_for_filename, get_role_abbreviation
from .paragraph_utils import copy_paragraph_with_relationships, copy_element_relationships
from .formatting_utils import (
    set_font_calibri_11pt,
    bold_paragraph,
    apply_bullet_style,
    is_intro_line,
    add_spacing_after,
)

__all__ = [
    "get_two_mondays_from_now",
    "format_date_for_filename",
    "backup_file",
    "find_word_files",
    "is_temp_file",
    "validate_docx",
    "ensure_subfolder_exists",
    "find_matching_subfolder",
    "sanitize_for_filename",
    "get_role_abbreviation",
    "copy_paragraph_with_relationships",
    "copy_element_relationships",
    "set_font_calibri_11pt",
    "bold_paragraph",
    "apply_bullet_style",
    "is_intro_line",
    "add_spacing_after",
]
