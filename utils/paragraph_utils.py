"""
Paragraph utility functions for copying with hyperlink preservation.
"""

from copy import deepcopy
from docx import Document


def copy_element_relationships(element, source_doc_part, target_doc_part):
    """
    Copy all relationships (hyperlinks, images, etc.) from source to target document.

    Args:
        element: The XML element that may contain relationships
        source_doc_part: The source document part (doc.part)
        target_doc_part: The target document part (new_doc.part)
    """
    # Define namespaces
    w_ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    r_ns = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'

    # Track which relationship IDs we've already processed to avoid duplicates
    processed_rels = {}

    # Find all hyperlink elements
    for hyperlink in element.iter(w_ns + 'hyperlink'):
        rel_id = hyperlink.get(r_ns + 'id')
        if rel_id:
            new_rel_id = _copy_relationship(rel_id, source_doc_part, target_doc_part, processed_rels)
            if new_rel_id:
                hyperlink.set(r_ns + 'id', new_rel_id)

    # Find all elements with r:embed (images)
    for elem in element.iter():
        embed_id = elem.get(r_ns + 'embed')
        if embed_id:
            new_rel_id = _copy_relationship(embed_id, source_doc_part, target_doc_part, processed_rels)
            if new_rel_id:
                elem.set(r_ns + 'embed', new_rel_id)

        # Also check for r:link attributes
        link_id = elem.get(r_ns + 'link')
        if link_id:
            new_rel_id = _copy_relationship(link_id, source_doc_part, target_doc_part, processed_rels)
            if new_rel_id:
                elem.set(r_ns + 'link', new_rel_id)


def _copy_relationship(rel_id, source_doc_part, target_doc_part, processed_rels):
    """
    Copy a single relationship from source to target document.

    Args:
        rel_id: The relationship ID to copy
        source_doc_part: The source document part
        target_doc_part: The target document part
        processed_rels: Dict tracking already processed relationships

    Returns:
        The new relationship ID, or None if copy failed
    """
    # Check if we've already processed this relationship
    if rel_id in processed_rels:
        return processed_rels[rel_id]

    try:
        # Get the relationship from the source document
        rel = source_doc_part.rels[rel_id]

        # Add the relationship to the target document
        new_rel_id = target_doc_part.relate_to(rel.target_ref, rel.reltype, rel.is_external)

        # Cache the mapping
        processed_rels[rel_id] = new_rel_id

        return new_rel_id
    except KeyError:
        # Relationship not found
        return None


def copy_paragraph_with_relationships(para, source_doc, target_doc):
    """
    Copy a paragraph from source to target document, preserving all relationships.

    This function handles hyperlinks, images, and other embedded content.

    Args:
        para: The paragraph to copy
        source_doc: The source Document object
        target_doc: The target Document object
    """
    # Deep copy the paragraph element to preserve all formatting
    new_para_element = deepcopy(para._element)

    # Copy all relationships before adding the paragraph
    copy_element_relationships(new_para_element, source_doc.part, target_doc.part)

    # Append to the target document body
    target_doc._body._body.append(new_para_element)


def copy_paragraph_with_formatting(source_para, target_doc):
    """
    Copy a paragraph with all its formatting to target document.

    Alternative method that creates a new paragraph and copies formatting properties.

    Args:
        source_para: The source paragraph
        target_doc: The target Document object

    Returns:
        The new paragraph in the target document
    """
    # Create new paragraph
    new_para = target_doc.add_paragraph()

    # Copy paragraph style
    try:
        new_para.style = source_para.style
    except Exception:
        pass  # Style may not exist in target document

    # Copy paragraph formatting
    pf = source_para.paragraph_format
    npf = new_para.paragraph_format

    if pf.alignment is not None:
        npf.alignment = pf.alignment
    if pf.left_indent is not None:
        npf.left_indent = pf.left_indent
    if pf.right_indent is not None:
        npf.right_indent = pf.right_indent
    if pf.first_line_indent is not None:
        npf.first_line_indent = pf.first_line_indent
    if pf.space_before is not None:
        npf.space_before = pf.space_before
    if pf.space_after is not None:
        npf.space_after = pf.space_after

    # Clear the new paragraph's content
    new_para._element.clear_content()

    # Copy all child elements from source to preserve hyperlinks and formatting
    for child in source_para._element:
        new_para._element.append(deepcopy(child))

    return new_para
