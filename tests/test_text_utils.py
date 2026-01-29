"""
Tests for text_utils.py

These tests challenge filename sanitization and role abbreviation with:
- Unicode characters
- Special characters
- Edge cases (empty strings, very long strings)
- All defined role mappings
- Case sensitivity
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.text_utils import sanitize_for_filename, get_role_abbreviation
from config import ROLE_ABBREVIATIONS


class TestSanitizeForFilename:
    """Tests for sanitize_for_filename function."""

    # Basic functionality tests
    def test_simple_text(self):
        """Test with simple alphanumeric text."""
        assert sanitize_for_filename("SimpleText") == "SimpleText"

    def test_spaces_replaced_with_underscores(self):
        """Test that spaces are replaced with underscores."""
        assert sanitize_for_filename("Hello World") == "Hello_World"

    def test_multiple_spaces(self):
        """Test handling of multiple consecutive spaces."""
        result = sanitize_for_filename("Hello   World")
        assert result == "Hello___World"

    def test_leading_trailing_whitespace_stripped(self):
        """Test that leading/trailing whitespace is stripped."""
        assert sanitize_for_filename("  Hello  ") == "Hello"

    def test_tabs_and_newlines(self):
        """Test handling of tabs and newlines."""
        result = sanitize_for_filename("Hello\tWorld\nTest")
        # Tabs and newlines should be removed as they're not alphanumeric
        assert "\t" not in result
        assert "\n" not in result

    # Special character tests
    @pytest.mark.parametrize("char", [
        "/", "\\", ":", "*", "?", '"', "<", ">", "|",
        "@", "#", "$", "%", "^", "&", "(", ")", "+", "=",
        "[", "]", "{", "}", ";", "'", ",", ".", "!", "`", "~"
    ])
    def test_special_characters_removed(self, char):
        """Test that problematic special characters are removed."""
        result = sanitize_for_filename(f"test{char}file")
        assert char not in result

    def test_hyphens_preserved(self):
        """Test that hyphens are preserved."""
        assert sanitize_for_filename("test-file-name") == "test-file-name"

    def test_underscores_preserved(self):
        """Test that underscores are preserved."""
        assert sanitize_for_filename("test_file_name") == "test_file_name"

    def test_numbers_preserved(self):
        """Test that numbers are preserved."""
        assert sanitize_for_filename("Test123File456") == "Test123File456"

    # Unicode tests - Note: Python's \w matches Unicode word characters by default
    @pytest.mark.parametrize("unicode_text", [
        "Caf\u00e9",       # e with acute
        "na\u00efve",      # i with diaeresis
        "r\u00e9sum\u00e9",  # multiple accents
        "\u4e2d\u6587",    # Chinese characters
        "\u0410\u0411\u0412",  # Cyrillic
        "\u03b1\u03b2\u03b3",  # Greek
    ])
    def test_unicode_characters_preserved(self, unicode_text):
        """Test that Unicode word characters are preserved (Python 3 \w behavior)."""
        result = sanitize_for_filename(unicode_text)
        # Python 3's \w matches Unicode word characters, so they're preserved
        # This documents the actual behavior
        assert len(result) > 0
        assert " " not in result

    def test_emoji_removed(self):
        """Test that emoji are removed."""
        result = sanitize_for_filename("test\U0001f600emoji")
        # Emoji are not word characters, so they should be removed
        assert result == "testemoji"

    def test_mixed_unicode_and_ascii(self):
        """Test text with mixed Unicode and ASCII."""
        result = sanitize_for_filename("Hello \u4e16\u754c World")
        # Chinese characters are preserved (Python 3 \w behavior)
        assert "Hello" in result
        assert "World" in result
        assert " " not in result  # Spaces converted to underscores

    # Edge cases
    def test_empty_string(self):
        """Test with empty string."""
        assert sanitize_for_filename("") == ""

    def test_whitespace_only(self):
        """Test with whitespace-only string."""
        assert sanitize_for_filename("   ") == ""
        assert sanitize_for_filename("\t\n") == ""

    def test_special_chars_only(self):
        """Test with only special characters."""
        result = sanitize_for_filename("@#$%^&*()")
        assert result == ""

    def test_very_long_string_truncated(self):
        """Test that very long strings are truncated to default max_length."""
        long_text = "A" * 1000
        result = sanitize_for_filename(long_text)
        assert len(result) == 100  # Default max_length
        assert result == "A" * 100

    def test_long_string_with_spaces(self):
        """Test long string with multiple spaces."""
        long_text = "Word " * 100
        result = sanitize_for_filename(long_text)
        assert "_" in result
        assert " " not in result
        assert len(result) <= 100

    def test_truncation_custom_length(self):
        """Test truncation with custom max_length."""
        text = "A" * 200
        result = sanitize_for_filename(text, max_length=50)
        assert len(result) == 50

    def test_truncation_disabled(self):
        """Test that truncation can be disabled."""
        long_text = "A" * 500
        result = sanitize_for_filename(long_text, max_length=0)
        assert len(result) == 500
        result = sanitize_for_filename(long_text, max_length=None)
        assert len(result) == 500

    def test_truncation_strips_trailing_underscores(self):
        """Test that truncation removes trailing underscores."""
        # Create text that will have underscore at position 100
        text = "A" * 99 + " B" * 50  # Space becomes underscore
        result = sanitize_for_filename(text)
        assert not result.endswith("_")

    def test_truncation_strips_trailing_hyphens(self):
        """Test that truncation removes trailing hyphens."""
        text = "A" * 99 + "-" + "B" * 50
        result = sanitize_for_filename(text)
        assert not result.endswith("-")

    def test_short_string_not_affected(self):
        """Test that strings under max_length are not affected."""
        text = "Short Title"
        result = sanitize_for_filename(text)
        assert result == "Short_Title"

    # Real-world heading tests
    @pytest.mark.parametrize("heading,expected", [
        ("Chief Audit Executive", "Chief_Audit_Executive"),
        ("CPO - Procurement (GBS)", "CPO_-_Procurement_GBS"),
        ("CPO - Product (HT)", "CPO_-_Product_HT"),
        ("R&D", "RD"),
        ("Customer Service", "Customer_Service"),
        ("General Counsel", "General_Counsel"),
        ("Tech CEO", "Tech_CEO"),
    ])
    def test_real_headings(self, heading, expected):
        """Test with actual headings from the application."""
        result = sanitize_for_filename(heading)
        assert result == expected

    def test_heading_with_colon(self):
        """Test heading with colon."""
        result = sanitize_for_filename("Title: Important Insight")
        assert result == "Title_Important_Insight"

    def test_heading_with_multiple_special_chars(self):
        """Test heading with multiple special characters."""
        result = sanitize_for_filename("Q&A: Best Practices (2024)")
        assert result == "QA_Best_Practices_2024"

    # Regression tests
    def test_preserves_case(self):
        """Test that case is preserved."""
        assert sanitize_for_filename("MixedCASE") == "MixedCASE"

    def test_consecutive_special_chars(self):
        """Test consecutive special characters."""
        result = sanitize_for_filename("test!!!file")
        assert result == "testfile"

    def test_special_char_at_boundaries(self):
        """Test special characters at start and end."""
        result = sanitize_for_filename("!test!")
        assert result == "test"


class TestGetRoleAbbreviation:
    """Tests for get_role_abbreviation function."""

    # Test all defined role mappings
    @pytest.mark.parametrize("role,expected", [
        ("Chief Audit Executive", "CAE"),
        ("CPO - Procurement (GBS)", "CPO_GBS"),
        ("CPO - Product (HT)", "CPO_GTS"),
        ("R&D", "RD"),
        ("Customer Service", "CS"),
        ("General Counsel", "GC"),
        ("Tech CEO", "TCEO"),
    ])
    def test_known_role_abbreviations(self, role, expected):
        """Test all defined role abbreviations."""
        result = get_role_abbreviation(role)
        assert result == expected

    def test_all_roles_in_config(self):
        """Verify we test all roles defined in config."""
        tested_roles = {
            "Chief Audit Executive", "CPO - Procurement (GBS)",
            "CPO - Product (HT)", "R&D", "Customer Service",
            "General Counsel", "Tech CEO"
        }
        assert tested_roles == set(ROLE_ABBREVIATIONS.keys())

    # Unknown roles fall back to sanitization
    def test_unknown_role_sanitized(self):
        """Test that unknown roles fall back to sanitize_for_filename."""
        result = get_role_abbreviation("Unknown Department")
        assert result == "Unknown_Department"

    def test_unknown_role_with_special_chars(self):
        """Test unknown role with special characters."""
        result = get_role_abbreviation("IT & Security (Team)")
        assert result == "IT__Security_Team"

    # Case sensitivity tests
    def test_case_sensitive_exact_match(self):
        """Verify role matching is case-sensitive."""
        # Lowercase should NOT match
        result = get_role_abbreviation("chief audit executive")
        assert result != "CAE"
        assert result == "chief_audit_executive"

    def test_mixed_case_no_match(self):
        """Test that mixed case doesn't match defined roles."""
        result = get_role_abbreviation("CHIEF AUDIT EXECUTIVE")
        assert result != "CAE"

    def test_partial_match_no_match(self):
        """Test that partial matches don't work."""
        result = get_role_abbreviation("Chief Audit")
        assert result == "Chief_Audit"

    def test_extra_whitespace_no_match(self):
        """Test that extra whitespace prevents matching."""
        result = get_role_abbreviation(" Chief Audit Executive ")
        # Leading/trailing spaces - won't match exact
        assert result == "Chief_Audit_Executive"

    # Edge cases
    def test_empty_string(self):
        """Test with empty string."""
        result = get_role_abbreviation("")
        assert result == ""

    def test_whitespace_only(self):
        """Test with whitespace-only string."""
        result = get_role_abbreviation("   ")
        assert result == ""

    def test_special_chars_only(self):
        """Test with only special characters."""
        result = get_role_abbreviation("@#$%")
        assert result == ""

    # Real-world scenarios
    @pytest.mark.parametrize("heading", [
        "VP of Engineering",
        "Senior Director - Marketing",
        "CISO (Information Security)",
        "Product Manager",
        "Head of Sales & Operations",
    ])
    def test_unknown_headings_sanitized(self, heading):
        """Test various unknown headings are properly sanitized."""
        result = get_role_abbreviation(heading)

        # Should be sanitized, not raise errors
        assert isinstance(result, str)
        assert " " not in result  # No spaces
        # Should not contain problematic chars
        for char in ['(', ')', '/', '\\', ':']:
            assert char not in result

    def test_very_long_role_name(self):
        """Test with a very long role name."""
        long_role = "Chief " + "Executive " * 50 + "Officer"
        result = get_role_abbreviation(long_role)

        assert isinstance(result, str)
        assert " " not in result

    def test_unicode_role_name(self):
        """Test role name with Unicode characters."""
        result = get_role_abbreviation("Directeur G\u00e9n\u00e9ral")
        # Should sanitize, removing non-ASCII
        assert isinstance(result, str)


class TestTextUtilsIntegration:
    """Integration tests for text utilities."""

    def test_role_to_filename_component(self):
        """Test using role abbreviation as part of a filename."""
        role = "Chief Audit Executive"
        abbrev = get_role_abbreviation(role)

        filename = f"1.15_{abbrev}_report.docx"
        assert filename == "1.15_CAE_report.docx"

    def test_unknown_role_to_filename(self):
        """Test using unknown role in filename generation."""
        role = "New Department (2024)"
        abbrev = get_role_abbreviation(role)

        filename = f"1.15_{abbrev}_report.docx"
        assert "(" not in filename
        assert ")" not in filename

    def test_sanitize_then_use_in_path(self):
        """Test that sanitized text is safe for file paths."""
        dangerous_input = "..\\..\\etc\\passwd"
        safe = sanitize_for_filename(dangerous_input)

        # Should not contain path traversal characters
        assert ".." not in safe or safe.count(".") == 0
        assert "\\" not in safe
        assert "/" not in safe

    def test_multiple_sanitizations_idempotent(self):
        """Test that sanitizing multiple times gives same result."""
        text = "Test & Report (2024)"
        first = sanitize_for_filename(text)
        second = sanitize_for_filename(first)
        third = sanitize_for_filename(second)

        assert first == second == third


class TestFilenameSecurityConcerns:
    """Security-focused tests for filename sanitization."""

    @pytest.mark.parametrize("dangerous_input", [
        "../../../etc/passwd",
        "..\\..\\windows\\system32",
        "file\x00name",  # Null byte
        "con",  # Windows reserved name
        "prn",  # Windows reserved name
        "aux",  # Windows reserved name
        "nul",  # Windows reserved name
        "com1",  # Windows reserved name
        "lpt1",  # Windows reserved name
    ])
    def test_dangerous_inputs(self, dangerous_input):
        """Test that dangerous inputs are sanitized."""
        result = sanitize_for_filename(dangerous_input)

        # Should not contain path traversal
        assert ".." not in result or not any(c in result for c in "/\\")
        # Should not contain null bytes
        assert "\x00" not in result

    def test_very_long_filename_truncated_for_safety(self):
        """Test that filenames are truncated to avoid filesystem limits."""
        # Most filesystems have 255 byte limit
        long_name = "A" * 300
        result = sanitize_for_filename(long_name)

        # Function now truncates to safe length (default 100)
        assert len(result) == 100

    def test_hidden_file_prefix(self):
        """Test handling of hidden file prefix (Unix)."""
        result = sanitize_for_filename(".hidden")
        # Dot is removed by sanitization
        assert result == "hidden"

    def test_command_injection_attempts(self):
        """Test that potential command injection is neutralized."""
        dangerous_inputs = [
            "; rm -rf /",
            "| cat /etc/passwd",
            "$(whoami)",
            "`id`",
            "file; echo pwned",
        ]

        for dangerous in dangerous_inputs:
            result = sanitize_for_filename(dangerous)
            assert ";" not in result
            assert "|" not in result
            assert "$" not in result
            assert "`" not in result
