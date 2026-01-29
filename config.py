"""
Configuration constants for Insight Processor.
"""

# Headers to bold in insight files
HEADERS_TO_BOLD = [
    "Why This Matters",
    "Implications",
    "Why Gartner",
    "Visual/Graphic",
    "Engage Clients and Prospects",
    "Probing Questions",
    "AskGartner Prompts to Recommend",
    "Insights to Engage",
]

# Sections to convert to bullets
# Format: (start_header, end_header_or_None)
# None means until the next header or end of document
BULLET_SECTIONS = [
    ("Why This Matters", "Implications"),
    ("Probing Questions", "AskGartner Prompts to Recommend"),
    ("AskGartner Prompts to Recommend", None),
]

# Role abbreviation mapping
ROLE_ABBREVIATIONS = {
    "Chief Audit Executive": "CAE",
    "CPO - Procurement (GBS)": "CPO_GBS",
    "CPO - Product (HT)": "CPO_GTS",
    "R&D": "RD",
    "Customer Service": "CS",
    "General Counsel": "GC",
    "Tech CEO": "TCEO",
}

# Formatting settings
FONT_NAME = "Calibri"
FONT_SIZE_PT = 11

# Email template heading patterns
EMAIL_HEADING_PATTERNS = {
    "BD": ["SALES BUSINESS DEVELOPER", "PROSPECT EMAIL"],
    "AE": ["SALES ACCOUNT EXECUTIVE", "CLIENT EMAIL"],
    "EP": ["SERVICE EXECUTIVE PARTNER", "CLIENT EMAIL"],
}
