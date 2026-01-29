"""
Tests for folder_utils.py

These tests challenge folder operations with:
- Case-insensitive matching
- Non-existent paths
- Permission issues
- Unicode folder names
- Edge cases
"""

import pytest
import os
import stat
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.folder_utils import ensure_subfolder_exists, find_matching_subfolder


class TestEnsureSubfolderExists:
    """Tests for ensure_subfolder_exists function."""

    def test_creates_new_subfolder(self, temp_dir):
        """Test creation of a new subfolder."""
        result = ensure_subfolder_exists(temp_dir, "new_folder")

        assert result.exists()
        assert result.is_dir()
        assert result.name == "new_folder"

    def test_returns_existing_subfolder(self, temp_dir):
        """Test that existing subfolder is returned unchanged."""
        # Create subfolder first
        existing = temp_dir / "existing"
        existing.mkdir()

        # Add a file to verify we got the same folder
        (existing / "marker.txt").write_text("marker")

        result = ensure_subfolder_exists(temp_dir, "existing")

        assert result == existing
        assert (result / "marker.txt").exists()

    def test_creates_nested_parents(self, temp_dir):
        """Test that parent directories are created if needed."""
        # Note: ensure_subfolder_exists uses mkdir(parents=True)
        # But it only creates one level of subfolder
        result = ensure_subfolder_exists(temp_dir, "new_subfolder")

        assert result.exists()
        assert result.parent == temp_dir

    def test_folder_with_spaces(self, temp_dir):
        """Test creation of folder with spaces in name."""
        result = ensure_subfolder_exists(temp_dir, "folder with spaces")

        assert result.exists()
        assert result.name == "folder with spaces"

    def test_folder_with_special_chars(self, temp_dir):
        """Test folder creation with allowed special characters."""
        # Some chars are OK in folder names
        result = ensure_subfolder_exists(temp_dir, "folder-name_v1")

        assert result.exists()
        assert result.name == "folder-name_v1"

    def test_folder_with_unicode(self, temp_dir):
        """Test folder creation with Unicode characters."""
        result = ensure_subfolder_exists(temp_dir, "folder_\u00e9\u00e0\u00fc")

        assert result.exists()

    def test_returns_correct_path_type(self, temp_dir):
        """Test that return value is a Path object."""
        result = ensure_subfolder_exists(temp_dir, "test")

        assert isinstance(result, Path)

    def test_idempotent(self, temp_dir):
        """Test that calling multiple times gives same result."""
        result1 = ensure_subfolder_exists(temp_dir, "folder")
        result2 = ensure_subfolder_exists(temp_dir, "folder")
        result3 = ensure_subfolder_exists(temp_dir, "folder")

        assert result1 == result2 == result3

    def test_empty_folder_name(self, temp_dir):
        """Test with empty folder name."""
        # This creates a folder with empty name, which resolves to parent
        result = ensure_subfolder_exists(temp_dir, "")

        # The result is temp_dir / "" which equals temp_dir
        assert result.exists()

    def test_folder_name_with_dots(self, temp_dir):
        """Test folder name containing dots."""
        result = ensure_subfolder_exists(temp_dir, "folder.name.v2")

        assert result.exists()
        assert result.name == "folder.name.v2"

    @pytest.mark.skipif(os.name == 'nt', reason="Test uses Unix-specific characters")
    def test_folder_with_most_special_chars(self, temp_dir):
        """Test folder with various special characters that are valid on Unix."""
        # These are valid on Unix but not Windows
        result = ensure_subfolder_exists(temp_dir, "folder!@#$%name")

        assert result.exists()


class TestFindMatchingSubfolder:
    """Tests for find_matching_subfolder function."""

    def test_exact_match(self, temp_dir):
        """Test finding a subfolder with exact name match."""
        subfolder = temp_dir / "MyFolder"
        subfolder.mkdir()

        result = find_matching_subfolder(temp_dir, "MyFolder")

        assert result == subfolder

    def test_case_insensitive_match_lowercase(self, temp_dir):
        """Test case-insensitive match with lowercase query."""
        subfolder = temp_dir / "MyFolder"
        subfolder.mkdir()

        result = find_matching_subfolder(temp_dir, "myfolder")

        # Should find a match (case-insensitive)
        assert result is not None
        assert result.name.lower() == "myfolder"

    def test_case_insensitive_match_uppercase(self, temp_dir):
        """Test case-insensitive match with uppercase query."""
        subfolder = temp_dir / "myfolder"
        subfolder.mkdir()

        result = find_matching_subfolder(temp_dir, "MYFOLDER")

        # Should find a match (case-insensitive)
        assert result is not None
        assert result.name.lower() == "myfolder"

    def test_case_insensitive_match_mixed(self, temp_dir):
        """Test case-insensitive match with mixed case."""
        subfolder = temp_dir / "MyFolder"
        subfolder.mkdir()

        result = find_matching_subfolder(temp_dir, "mYfOLDER")

        # Should find a match (case-insensitive)
        assert result is not None
        assert result.name.lower() == "myfolder"

    def test_no_match_returns_none(self, temp_dir):
        """Test that non-existent subfolder returns None."""
        (temp_dir / "other_folder").mkdir()

        result = find_matching_subfolder(temp_dir, "nonexistent")

        assert result is None

    def test_parent_not_exists(self, temp_dir):
        """Test with non-existent parent directory."""
        non_existent = temp_dir / "does_not_exist"

        result = find_matching_subfolder(non_existent, "subfolder")

        assert result is None

    def test_parent_is_file(self, temp_dir):
        """Test when parent path is a file, not a directory."""
        file_path = temp_dir / "a_file.txt"
        file_path.write_text("content")

        result = find_matching_subfolder(file_path, "subfolder")

        assert result is None

    def test_prefers_exact_match_over_case_insensitive(self, temp_dir):
        """Test that exact match is preferred when both exist."""
        # Note: On case-insensitive filesystems (macOS default), only one can exist
        exact = temp_dir / "MyFolder"
        exact.mkdir()

        result = find_matching_subfolder(temp_dir, "MyFolder")

        # Should find exact match
        assert result is not None
        assert result.name == "MyFolder"

    def test_finds_file_not_directory_returns_none(self, temp_dir):
        """Test that files are not returned, only directories."""
        # Create a file with the target name
        file_path = temp_dir / "target"
        file_path.write_text("content")

        result = find_matching_subfolder(temp_dir, "target")

        assert result is None

    def test_multiple_similar_names(self, temp_dir):
        """Test with folders that have similar but distinct names."""
        # On case-insensitive filesystems, only distinct names can coexist
        (temp_dir / "report").mkdir()
        (temp_dir / "reports").mkdir()  # Different name (plural)

        # Should find exact match
        result = find_matching_subfolder(temp_dir, "report")
        assert result is not None
        assert result.name.lower() == "report"

        result = find_matching_subfolder(temp_dir, "reports")
        assert result is not None
        assert result.name.lower() == "reports"

    def test_folder_with_spaces(self, temp_dir):
        """Test finding folder with spaces."""
        subfolder = temp_dir / "My Folder Name"
        subfolder.mkdir()

        result = find_matching_subfolder(temp_dir, "My Folder Name")
        assert result is not None
        assert result.name == "My Folder Name"

        result_lower = find_matching_subfolder(temp_dir, "my folder name")
        assert result_lower is not None
        assert result_lower.name.lower() == "my folder name"

    def test_folder_with_unicode(self, temp_dir):
        """Test finding folder with Unicode characters."""
        subfolder = temp_dir / "Caf\u00e9"
        subfolder.mkdir()

        result = find_matching_subfolder(temp_dir, "Caf\u00e9")
        assert result == subfolder

    def test_empty_directory(self, temp_dir):
        """Test finding subfolder in empty directory."""
        result = find_matching_subfolder(temp_dir, "anything")

        assert result is None

    def test_nested_not_found(self, temp_dir):
        """Test that nested subfolders are not searched."""
        nested = temp_dir / "parent" / "child"
        nested.mkdir(parents=True)

        # Should not find nested "child" folder
        result = find_matching_subfolder(temp_dir, "child")

        assert result is None

    def test_real_role_names(self, temp_dir):
        """Test with actual role names from the application."""
        roles = [
            "Chief Audit Executive",
            "CPO - Procurement (GBS)",
            "CPO - Product (HT)",
            "R&D",
            "Customer Service",
            "General Counsel",
            "Tech CEO",
        ]

        for role in roles:
            (temp_dir / role).mkdir()

        for role in roles:
            result = find_matching_subfolder(temp_dir, role)
            assert result is not None
            assert result.name == role

    def test_role_name_case_variants(self, temp_dir):
        """Test finding role folders with different cases."""
        (temp_dir / "Chief Audit Executive").mkdir()

        variants = [
            "Chief Audit Executive",
            "chief audit executive",
            "CHIEF AUDIT EXECUTIVE",
            "cHiEf AuDiT eXeCuTiVe",
        ]

        for variant in variants:
            result = find_matching_subfolder(temp_dir, variant)
            assert result is not None, f"Failed to find with: {variant}"


class TestFolderUtilsIntegration:
    """Integration tests for folder utilities."""

    def test_ensure_then_find(self, temp_dir):
        """Test creating a folder and then finding it."""
        created = ensure_subfolder_exists(temp_dir, "NewFolder")
        found = find_matching_subfolder(temp_dir, "NewFolder")

        assert created == found

    def test_ensure_then_find_case_insensitive(self, temp_dir):
        """Test creating folder and finding with different case."""
        created = ensure_subfolder_exists(temp_dir, "MyFolder")
        found = find_matching_subfolder(temp_dir, "myfolder")

        # Both should refer to the same folder (case-insensitive match)
        assert found is not None
        assert found.name.lower() == created.name.lower()

    def test_typical_workflow(self, temp_dir):
        """Test typical usage pattern from the application."""
        # Create role folders
        roles = ["Chief Audit Executive", "General Counsel"]

        for role in roles:
            ensure_subfolder_exists(temp_dir, role)

        # Later, find them (possibly with different case)
        cae = find_matching_subfolder(temp_dir, "chief audit executive")
        gc = find_matching_subfolder(temp_dir, "GENERAL COUNSEL")

        assert cae is not None
        assert gc is not None

    def test_multiple_ensure_calls(self, temp_dir):
        """Test multiple ensure calls don't create duplicates."""
        for _ in range(5):
            ensure_subfolder_exists(temp_dir, "folder")

        # Count subfolders
        subfolders = [p for p in temp_dir.iterdir() if p.is_dir()]
        assert len(subfolders) == 1
