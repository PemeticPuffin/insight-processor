"""
Formatting utility functions for fonts, bullets, and headers.
"""

import re
from docx.shared import Pt, Inches
from docx.oxml.ns import qn
from config import FONT_NAME, FONT_SIZE_PT

# Bullet character for manual bullet formatting
BULLET_CHAR = '\u2022'  # •


def set_font_calibri_11pt(paragraph):
    """
    Set all runs in a paragraph to Calibri 11pt font.

    Args:
        paragraph: The paragraph to format
    """
    for run in paragraph.runs:
        run.font.name = FONT_NAME
        run.font.size = Pt(FONT_SIZE_PT)


def bold_paragraph(paragraph):
    """
    Make all runs in a paragraph bold.

    Args:
        paragraph: The paragraph to bold
    """
    for run in paragraph.runs:
        run.bold = True


def clear_all_list_formatting(paragraph):
    """
    Aggressively remove ALL list-related formatting from a paragraph.

    This clears numPr and any other list-related elements from the paragraph XML.
    Also removes the pStyle if it references a list style.

    Args:
        paragraph: The paragraph to clear list formatting from
    """
    p_element = paragraph._element
    pPr = p_element.find(qn('w:pPr'))

    if pPr is not None:
        # Remove numPr (numbering properties)
        for num_element in pPr.findall(qn('w:numPr')):
            pPr.remove(num_element)

        # Remove any list-related style references
        for pStyle in pPr.findall(qn('w:pStyle')):
            style_val = pStyle.get(qn('w:val'), '')
            if 'List' in style_val or 'Bullet' in style_val or 'Number' in style_val:
                pPr.remove(pStyle)

    # Also check for numPr directly under the paragraph element (rare but possible)
    for num_element in p_element.findall(qn('w:numPr')):
        p_element.remove(num_element)


def apply_bullet_style(paragraph):
    """
    Apply bullet point formatting to a paragraph.

    Uses a completely fresh approach to avoid any residual list formatting:
    1. Extracts the plain text
    2. Clears ALL paragraph content and formatting
    3. Rebuilds with bullet character and clean formatting

    Args:
        paragraph: The paragraph to convert to a bullet
    """
    # Get the plain text content (strip any existing bullet chars)
    text = paragraph.text
    if text.startswith(BULLET_CHAR):
        text = text[1:].lstrip('\t ')

    # Aggressively clear all list formatting
    clear_all_list_formatting(paragraph)

    # Set to Normal style
    paragraph.style = 'Normal'

    # Clear again after style change (style can re-add formatting)
    clear_all_list_formatting(paragraph)

    # Now completely clear and rebuild the paragraph content
    paragraph.clear()

    # Add fresh run with bullet character, tab, and text
    run = paragraph.add_run(BULLET_CHAR + '\t' + text.strip())
    run.font.name = FONT_NAME
    run.font.size = Pt(FONT_SIZE_PT)

    # Clear any list formatting one more time (to be absolutely sure)
    clear_all_list_formatting(paragraph)

    # Set indentation for bullet appearance
    paragraph.paragraph_format.left_indent = Inches(0.5)
    paragraph.paragraph_format.first_line_indent = Inches(-0.25)


def is_intro_line(text: str, is_first_in_section: bool = False) -> bool:
    """
    Detect if a line is an intro line that should not be bulleted.

    Intro lines are detected by:
    - Ending with a colon (:)
    - Being a section intro phrase (e.g., "Here are", "The following")
    - Being the first line of a section AND being a complete sentence
    - Being a full sentence with explanatory context (contains "you/your")

    Args:
        text: The text to check
        is_first_in_section: True if this is the first non-empty paragraph after a section header

    Returns:
        True if this appears to be an intro line
    """
    text = text.strip()

    if not text:
        return False

    # Check if ends with colon (intro phrase)
    if text.endswith(':'):
        return True

    # Check for common intro patterns
    intro_patterns = [
        r'^Here\s+(are|is)\b',
        r'^The\s+following\b',
        r'^Consider\s+the\s+following\b',
        r'^Below\s+(are|is)\b',
        r'^This\s+includes?\b',
    ]

    for pattern in intro_patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return True

    # Check if it's a full sentence ending with a period
    if text.endswith('.'):
        words = text.split()

        # If this is the first line in a section and it's a complete sentence,
        # treat it as an intro line (these are typically context-setting sentences)
        if is_first_in_section and len(words) >= 4:
            # Check if it doesn't look like a bullet point (doesn't start with action verbs)
            action_verbs = ['use', 'apply', 'create', 'develop', 'implement',
                          'analyze', 'review', 'ensure', 'provide', 'manage',
                          'identify', 'define', 'establish', 'build', 'leverage',
                          'drive', 'enable', 'support', 'deliver', 'achieve']
            first_word = words[0].lower().rstrip('.,;:')
            if first_word not in action_verbs:
                return True

        # Full sentences typically have at least 5 words and don't start with action verbs
        # commonly used in bullet points
        if len(words) >= 5:
            # Check if it doesn't start with typical bullet-point action verbs
            action_verbs = ['use', 'apply', 'create', 'develop', 'implement',
                          'analyze', 'review', 'ensure', 'provide', 'manage',
                          'identify', 'define', 'establish', 'build', 'leverage',
                          'drive', 'enable', 'support', 'deliver', 'achieve']
            first_word = words[0].lower().rstrip('.,;:')
            if first_word not in action_verbs:
                # Additional check: if it contains "you" or "your" in an explanatory context
                if 'you' in text.lower() or 'your' in text.lower():
                    return True

    return False


def add_spacing_after(paragraph, points: int = 12):
    """
    Add spacing after a paragraph.

    Args:
        paragraph: The paragraph to add spacing to
        points: The amount of spacing in points (default 12)
    """
    paragraph.paragraph_format.space_after = Pt(points)


def is_numbered_or_dashed_list(paragraph) -> bool:
    """
    Check if a paragraph is a numbered list or uses dashes as bullets.

    Args:
        paragraph: The paragraph to check

    Returns:
        True if the paragraph uses numbers or dashes as list markers
    """
    text = paragraph.text.strip()

    if not text:
        return False

    # Check for numbered list patterns (1. or 1) or a. or a))
    numbered_patterns = [
        r'^\d+[\.\)]\s',      # 1. or 1)
        r'^[a-zA-Z][\.\)]\s',  # a. or a)
        r'^\(\d+\)\s',         # (1)
        r'^\([a-zA-Z]\)\s',    # (a)
    ]

    for pattern in numbered_patterns:
        if re.match(pattern, text):
            return True

    # Check for dash/hyphen bullet
    if text.startswith('- ') or text.startswith('– ') or text.startswith('— '):
        return True

    return False


def convert_to_dot_bullet(paragraph):
    """
    Convert a numbered or dashed list item to a dot bullet.

    Removes the existing marker and applies bullet style.
    Preserves bold formatting if present.

    Args:
        paragraph: The paragraph to convert
    """
    text = paragraph.text.strip()

    # Preserve bold state before clearing
    is_bold = False
    if paragraph.runs:
        is_bold = paragraph.runs[0].bold

    # Remove numbered list markers
    numbered_patterns = [
        r'^\d+[\.\)]\s*',
        r'^[a-zA-Z][\.\)]\s*',
        r'^\(\d+\)\s*',
        r'^\([a-zA-Z]\)\s*',
    ]

    for pattern in numbered_patterns:
        text = re.sub(pattern, '', text)

    # Remove dash/hyphen markers
    if text.startswith('- '):
        text = text[2:]
    elif text.startswith('– ') or text.startswith('— '):
        text = text[2:]

    # Clear and set clean text (apply_bullet_style will rebuild)
    paragraph.clear()
    paragraph.add_run(text.strip())

    # Apply bullet style (this will clear and rebuild with bullet char)
    apply_bullet_style(paragraph)

    # Re-apply bold if it was set
    if is_bold and paragraph.runs:
        for run in paragraph.runs:
            run.bold = True
