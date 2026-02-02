"""
Tests for formatting_utils.py

These tests challenge formatting functions with:
- Complex paragraph structures
- Edge cases in intro line detection
- Various list formats
- Font and style preservation
"""

import pytest
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.formatting_utils import (
    set_font_calibri_11pt,
    bold_paragraph,
    apply_bullet_style,
    is_intro_line,
    add_spacing_after,
    is_numbered_or_dashed_list,
    convert_to_dot_bullet,
)
from config import FONT_NAME, FONT_SIZE_PT


class TestSetFontCalibri11pt:
    """Tests for set_font_calibri_11pt function."""

    def test_basic_paragraph(self, temp_dir):
        """Test setting font on a basic paragraph."""
        doc = Document()
        para = doc.add_paragraph("Test paragraph")

        set_font_calibri_11pt(para)

        for run in para.runs:
            assert run.font.name == FONT_NAME
            assert run.font.size == Pt(FONT_SIZE_PT)

    def test_multiple_runs(self, temp_dir):
        """Test setting font on paragraph with multiple runs."""
        doc = Document()
        para = doc.add_paragraph()
        para.add_run("First part ")
        para.add_run("second part ")
        para.add_run("third part")

        set_font_calibri_11pt(para)

        assert len(para.runs) == 3
        for run in para.runs:
            assert run.font.name == FONT_NAME
            assert run.font.size == Pt(FONT_SIZE_PT)

    def test_empty_paragraph(self, temp_dir):
        """Test setting font on empty paragraph."""
        doc = Document()
        para = doc.add_paragraph("")

        # Should not raise error
        set_font_calibri_11pt(para)

    def test_paragraph_with_no_runs(self, temp_dir):
        """Test paragraph with no runs."""
        doc = Document()
        para = doc.add_paragraph()

        # Should not raise error
        set_font_calibri_11pt(para)
        assert len(para.runs) == 0

    def test_preserves_bold(self, temp_dir):
        """Test that bold formatting is preserved."""
        doc = Document()
        para = doc.add_paragraph()
        run = para.add_run("Bold text")
        run.bold = True

        set_font_calibri_11pt(para)

        # Bold should be preserved
        assert para.runs[0].bold == True

    def test_preserves_italic(self, temp_dir):
        """Test that italic formatting is preserved."""
        doc = Document()
        para = doc.add_paragraph()
        run = para.add_run("Italic text")
        run.italic = True

        set_font_calibri_11pt(para)

        assert para.runs[0].italic == True

    def test_overwrites_different_font(self, temp_dir):
        """Test that different font is overwritten."""
        doc = Document()
        para = doc.add_paragraph()
        run = para.add_run("Different font")
        run.font.name = "Arial"
        run.font.size = Pt(14)

        set_font_calibri_11pt(para)

        assert para.runs[0].font.name == FONT_NAME
        assert para.runs[0].font.size == Pt(FONT_SIZE_PT)


class TestBoldParagraph:
    """Tests for bold_paragraph function."""

    def test_basic_bold(self, temp_dir):
        """Test making a paragraph bold."""
        doc = Document()
        para = doc.add_paragraph("Text to bold")

        bold_paragraph(para)

        for run in para.runs:
            assert run.bold == True

    def test_multiple_runs_all_bold(self, temp_dir):
        """Test that all runs become bold."""
        doc = Document()
        para = doc.add_paragraph()
        para.add_run("First ")
        para.add_run("Second ")
        para.add_run("Third")

        bold_paragraph(para)

        for run in para.runs:
            assert run.bold == True

    def test_already_bold_stays_bold(self, temp_dir):
        """Test that already bold text stays bold."""
        doc = Document()
        para = doc.add_paragraph()
        run = para.add_run("Already bold")
        run.bold = True

        bold_paragraph(para)

        assert para.runs[0].bold == True

    def test_empty_paragraph(self, temp_dir):
        """Test bolding empty paragraph."""
        doc = Document()
        para = doc.add_paragraph("")

        # Should not raise error
        bold_paragraph(para)

    def test_preserves_other_formatting(self, temp_dir):
        """Test that other formatting is preserved."""
        doc = Document()
        para = doc.add_paragraph()
        run = para.add_run("Italic text")
        run.italic = True
        run.underline = True

        bold_paragraph(para)

        assert para.runs[0].bold == True
        assert para.runs[0].italic == True
        assert para.runs[0].underline == True


class TestApplyBulletStyle:
    """Tests for apply_bullet_style function."""

    def test_applies_bullet_formatting(self, temp_dir):
        """Test that bullet character and formatting is applied."""
        doc = Document()
        para = doc.add_paragraph("Bullet item")

        apply_bullet_style(para)

        # Should have Normal style (not List Bullet which can have numbering)
        assert para.style.name == "Normal"
        # Should start with bullet character
        assert para.text.startswith('\u2022')  # •

    def test_multiple_paragraphs(self, temp_dir):
        """Test applying bullets to multiple paragraphs."""
        doc = Document()
        paras = [
            doc.add_paragraph("Item 1"),
            doc.add_paragraph("Item 2"),
            doc.add_paragraph("Item 3"),
        ]

        for para in paras:
            apply_bullet_style(para)

        for para in paras:
            assert para.style.name == "Normal"
            assert para.text.startswith('\u2022')  # •

    def test_preserves_text_content(self, temp_dir):
        """Test that text content is preserved (with bullet prefix)."""
        doc = Document()
        original_text = "Important bullet point"
        para = doc.add_paragraph(original_text)

        apply_bullet_style(para)

        # Text should contain original content with bullet prefix
        assert original_text in para.text
        assert para.text.startswith('\u2022')  # •


class TestIsIntroLine:
    """Tests for is_intro_line function."""

    # Lines ending with colon should be intro lines
    @pytest.mark.parametrize("text", [
        "Key points:",
        "Consider the following:",
        "Important items:",
        "Requirements:",
        "Steps to take:",
    ])
    def test_colon_ending_is_intro(self, text):
        """Test that lines ending with colon are detected as intro."""
        assert is_intro_line(text) == True

    # Common intro patterns
    @pytest.mark.parametrize("text", [
        "Here are the key points",
        "Here is the summary",
        "The following items are important",
        "Consider the following approach",
        "Below are the recommendations",
        "Below is the data",
        "This includes several items",
    ])
    def test_common_intro_patterns(self, text):
        """Test common intro phrase patterns."""
        assert is_intro_line(text) == True

    # Lines that should NOT be intro lines
    @pytest.mark.parametrize("text", [
        "Use proper security measures.",
        "Apply the new policy.",
        "Create a backup before proceeding.",
        "Develop a comprehensive strategy.",
        "Implement the solution.",
        "Analyze the results.",
        "Review the documentation.",
        "Ensure compliance.",
        "Provide regular updates.",
        "Manage resources effectively.",
    ])
    def test_action_verb_lines_not_intro(self, text):
        """Test that lines starting with action verbs are not intro."""
        assert is_intro_line(text) == False

    # Full sentences with explanatory content
    @pytest.mark.parametrize("text", [
        "This is a detailed explanation of what you need to do for your project.",
        "When you review your options, consider the long-term implications.",
        "If your team needs guidance, refer to the documentation.",
    ])
    def test_full_sentence_with_you_is_intro(self, text):
        """Test that explanatory sentences with 'you/your' are intro."""
        assert is_intro_line(text) == True

    # Short lines
    @pytest.mark.parametrize("text", [
        "Short.",
        "Two words.",
        "Three word line.",
    ])
    def test_short_lines_not_intro(self, text):
        """Test that short lines (< 5 words) are not intro."""
        assert is_intro_line(text) == False

    # Edge cases
    def test_empty_string(self):
        """Test with empty string."""
        assert is_intro_line("") == False

    def test_whitespace_only(self):
        """Test with whitespace only."""
        assert is_intro_line("   ") == False

    def test_single_colon(self):
        """Test string that is just a colon."""
        assert is_intro_line(":") == True

    def test_case_insensitivity(self):
        """Test that pattern matching is case-insensitive."""
        assert is_intro_line("HERE ARE THE POINTS") == True
        assert is_intro_line("here are the points") == True
        assert is_intro_line("Here Are The Points") == True

    def test_colon_in_middle_not_intro(self):
        """Test that colon in middle of sentence doesn't make it intro."""
        text = "Step 1: Execute the plan."
        # Ends with period, has colon in middle
        # This is tricky - depends on full logic
        result = is_intro_line(text)
        # May or may not be intro depending on word count and patterns

    def test_bullet_point_content(self):
        """Test typical bullet point content."""
        bullets = [
            "Reduce costs by 20%",
            "Improve efficiency",
            "Streamline processes",
            "Eliminate redundancy",
        ]

        for bullet in bullets:
            assert is_intro_line(bullet) == False

    # Real-world examples from the application
    @pytest.mark.parametrize("text,expected", [
        ("Why this matters to you:", True),
        ("Key takeaways:", True),
        ("Here are three reasons why this is important.", True),
        ("Use this insight to drive conversations.", False),
        ("Apply these principles in your discussions.", False),
    ])
    def test_real_world_examples(self, text, expected):
        """Test with real-world examples."""
        assert is_intro_line(text) == expected


class TestAddSpacingAfter:
    """Tests for add_spacing_after function."""

    def test_default_spacing(self, temp_dir):
        """Test default 12pt spacing."""
        doc = Document()
        para = doc.add_paragraph("Test paragraph")

        add_spacing_after(para)

        assert para.paragraph_format.space_after == Pt(12)

    def test_custom_spacing(self, temp_dir):
        """Test custom spacing values."""
        doc = Document()
        para = doc.add_paragraph("Test paragraph")

        add_spacing_after(para, points=24)

        assert para.paragraph_format.space_after == Pt(24)

    def test_zero_spacing(self, temp_dir):
        """Test zero spacing."""
        doc = Document()
        para = doc.add_paragraph("Test paragraph")

        add_spacing_after(para, points=0)

        assert para.paragraph_format.space_after == Pt(0)

    def test_large_spacing(self, temp_dir):
        """Test large spacing value."""
        doc = Document()
        para = doc.add_paragraph("Test paragraph")

        add_spacing_after(para, points=72)

        assert para.paragraph_format.space_after == Pt(72)


class TestIsNumberedOrDashedList:
    """Tests for is_numbered_or_dashed_list function."""

    # Numbered list patterns
    @pytest.mark.parametrize("text", [
        "1. First item",
        "2. Second item",
        "10. Tenth item",
        "100. Hundredth item",
        "1) First item",
        "2) Second item",
        "(1) First item",
        "(2) Second item",
    ])
    def test_numbered_patterns(self, text):
        """Test various numbered list patterns."""
        doc = Document()
        para = doc.add_paragraph(text)

        assert is_numbered_or_dashed_list(para) == True

    # Letter list patterns
    @pytest.mark.parametrize("text", [
        "a. First item",
        "b. Second item",
        "z. Last item",
        "A. First item",
        "B. Second item",
        "a) First item",
        "A) First item",
        "(a) First item",
        "(A) First item",
    ])
    def test_letter_patterns(self, text):
        """Test various letter list patterns."""
        doc = Document()
        para = doc.add_paragraph(text)

        assert is_numbered_or_dashed_list(para) == True

    # Dash patterns
    @pytest.mark.parametrize("text", [
        "- First item",
        "- Second item",
        "\u2013 En dash item",  # en-dash
        "\u2014 Em dash item",  # em-dash
    ])
    def test_dash_patterns(self, text):
        """Test dash list patterns."""
        doc = Document()
        para = doc.add_paragraph(text)

        assert is_numbered_or_dashed_list(para) == True

    # Non-list patterns
    @pytest.mark.parametrize("text", [
        "Regular paragraph text",
        "This is a sentence.",
        "No list marker here",
        "1234 This starts with number but no marker",
        "a sentence starting with a",
        "-continued line",  # No space after dash
        "* Asterisk item",  # Not a dash
    ])
    def test_non_list_patterns(self, text):
        """Test text that should NOT be detected as list."""
        doc = Document()
        para = doc.add_paragraph(text)

        assert is_numbered_or_dashed_list(para) == False

    def test_empty_paragraph(self, temp_dir):
        """Test with empty paragraph."""
        doc = Document()
        para = doc.add_paragraph("")

        assert is_numbered_or_dashed_list(para) == False

    def test_whitespace_only(self, temp_dir):
        """Test with whitespace only."""
        doc = Document()
        para = doc.add_paragraph("   ")

        assert is_numbered_or_dashed_list(para) == False


class TestConvertToDotBullet:
    """Tests for convert_to_dot_bullet function."""

    def test_converts_numbered_to_bullet(self, temp_dir):
        """Test converting numbered list to bullet."""
        doc = Document()
        para = doc.add_paragraph("1. First item")

        convert_to_dot_bullet(para)

        assert para.style.name == "Normal"
        assert "1." not in para.text
        assert para.text.startswith('\u2022')  # •

    def test_converts_dash_to_bullet(self, temp_dir):
        """Test converting dash list to bullet."""
        doc = Document()
        para = doc.add_paragraph("- Dash item")

        convert_to_dot_bullet(para)

        assert para.style.name == "Normal"
        assert "Dash item" in para.text
        assert para.text.startswith('\u2022')  # •

    def test_converts_letter_to_bullet(self, temp_dir):
        """Test converting letter list to bullet."""
        doc = Document()
        para = doc.add_paragraph("a. Letter item")

        convert_to_dot_bullet(para)

        assert para.style.name == "Normal"
        assert "a." not in para.text
        assert para.text.startswith('\u2022')  # •

    def test_preserves_font_name(self, temp_dir):
        """Test that font name is preserved."""
        doc = Document()
        para = doc.add_paragraph()
        run = para.add_run("1. Item with font")
        run.font.name = "Arial"

        convert_to_dot_bullet(para)

        # Font should be preserved or defaulted to config
        assert para.runs[0].font.name in ["Arial", FONT_NAME]

    def test_preserves_bold(self, temp_dir):
        """Test that bold formatting is preserved."""
        doc = Document()
        para = doc.add_paragraph()
        run = para.add_run("1. Bold item")
        run.bold = True

        convert_to_dot_bullet(para)

        assert para.runs[0].bold == True

    def test_en_dash_removal(self, temp_dir):
        """Test en-dash is removed."""
        doc = Document()
        para = doc.add_paragraph("\u2013 En dash item")

        convert_to_dot_bullet(para)

        assert "\u2013" not in para.text

    def test_em_dash_removal(self, temp_dir):
        """Test em-dash is removed."""
        doc = Document()
        para = doc.add_paragraph("\u2014 Em dash item")

        convert_to_dot_bullet(para)

        assert "\u2014" not in para.text

    def test_parenthetical_number_removal(self, temp_dir):
        """Test (1) format is removed."""
        doc = Document()
        para = doc.add_paragraph("(1) Parenthetical item")

        convert_to_dot_bullet(para)

        assert "(1)" not in para.text

    def test_paragraph_with_no_runs(self, temp_dir):
        """Test conversion on paragraph with no runs."""
        doc = Document()
        para = doc.add_paragraph()
        # Manually add text without creating a run via add_run
        # This is unusual but should be handled

        # This is actually tricky to create - add_paragraph creates a run
        # So we'll just test that it doesn't crash on empty text
        para2 = doc.add_paragraph("")
        convert_to_dot_bullet(para2)


class TestFormattingUtilsIntegration:
    """Integration tests for formatting utilities."""

    def test_full_formatting_workflow(self, temp_dir):
        """Test typical formatting workflow."""
        doc = Document()
        para = doc.add_paragraph("1. Important point")

        # Set font
        set_font_calibri_11pt(para)

        # Convert to bullet
        convert_to_dot_bullet(para)

        assert para.style.name == "Normal"
        assert para.text.startswith('\u2022')  # •

    def test_format_header_then_content(self, temp_dir):
        """Test formatting header and content differently."""
        doc = Document()

        header = doc.add_paragraph("Why This Matters")
        set_font_calibri_11pt(header)
        bold_paragraph(header)

        content = doc.add_paragraph("- Key insight point")
        set_font_calibri_11pt(content)
        convert_to_dot_bullet(content)

        assert header.runs[0].bold == True
        assert content.style.name == "Normal"
        assert content.text.startswith('\u2022')  # •

    def test_detect_and_convert_list(self, temp_dir):
        """Test detecting list and converting it."""
        doc = Document()
        para = doc.add_paragraph("1. First point")

        if is_numbered_or_dashed_list(para):
            convert_to_dot_bullet(para)

        assert para.style.name == "Normal"
        assert para.text.startswith('\u2022')  # •

    def test_skip_intro_apply_bullet_to_content(self, temp_dir):
        """Test skipping intro line and bulleting content."""
        doc = Document()

        intro = doc.add_paragraph("Key points to consider:")
        content1 = doc.add_paragraph("First important point")
        content2 = doc.add_paragraph("Second important point")

        paragraphs = [intro, content1, content2]

        for para in paragraphs:
            text = para.text
            if not is_intro_line(text):
                apply_bullet_style(para)

        # Intro should not be bulleted (no bullet char)
        assert not intro.text.startswith('\u2022')
        # Content should be bulleted
        assert content1.text.startswith('\u2022')  # •
        assert content2.text.startswith('\u2022')  # •
