"""
File utility functions for discovery, backup, and validation.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import List


def backup_file(path: Path) -> Path:
    """
    Create a backup of a file with timestamp.

    Args:
        path: Path to the file to backup

    Returns:
        Path to the backup file
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{path.stem}_backup_{timestamp}{path.suffix}"
    backup_path = path.parent / backup_name

    # Copy the file
    import shutil
    shutil.copy2(path, backup_path)

    return backup_path


def find_word_files(directory: Path, recursive: bool = True) -> List[Path]:
    """
    Find all Word documents in a directory.

    Args:
        directory: Directory to search in
        recursive: If True, search subdirectories recursively

    Returns:
        List of paths to .docx files (excluding temp files)
    """
    word_files = []

    if recursive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.docx') and not is_temp_file(file):
                    word_files.append(Path(root) / file)
    else:
        for file in directory.iterdir():
            if file.is_file() and file.suffix == '.docx' and not is_temp_file(file.name):
                word_files.append(file)

    return sorted(word_files, key=lambda p: p.stat().st_mtime, reverse=True)


def is_temp_file(filename: str) -> bool:
    """
    Check if a filename is a temporary Word file.

    Args:
        filename: The filename to check

    Returns:
        True if the file is a temp file (starts with ~$)
    """
    return filename.startswith('~$')


def validate_docx(path: Path) -> bool:
    """
    Validate that a file is a valid Word document.

    Args:
        path: Path to the file to validate

    Returns:
        True if the file is a valid .docx file
    """
    if not path.exists():
        return False

    if path.suffix.lower() != '.docx':
        return False

    # Try to open the document to verify it's valid
    try:
        from docx import Document
        doc = Document(path)
        return True
    except Exception:
        return False
