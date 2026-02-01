"""
Configuration constants for Insight Processor.
"""

# Headers to bold in insight files
HEADERS_TO_BOLD = [
    "Top Insights to Engage",
    "Why This Matters",
    "Implications",
    "Why Gartner",
    "Visual/Graphic",
    "Engage Clients and Prospects",
    "Probing Questions",
    "AskGartner Prompts to Recommend",
    "Insights to Engage",
    "Key Terms",
]

# Section headers whose content should be bulleted
# Content is bulleted from each header until the next header in HEADERS_TO_BOLD
BULLET_SECTION_HEADERS = [
    "Why This Matters",
    "Implications",
    "Probing Questions",
    "AskGartner Prompts to Recommend",
    "Key Terms",
]

# Role folder definitions: (create_name, [all_synonyms])
# - create_name: the folder name to create if none exists
# - all_synonyms: all variations of the role name (for input matching AND folder searching)
# Matching is case-insensitive and exact (not substring)
ROLE_FOLDER_DEFINITIONS = [
    ("CIO", ["CIO"]),
    ("TCMO", ["Tech CMO", "TCMO"]),
    ("CHRO", ["CHRO"]),
    ("CSCO", ["CSCO"]),
    ("CMO", ["CMO"]),
    ("CS", ["Customer Service", "CS"]),
    ("RD", ["R&D", "RND", "RD"]),
    ("CAE", ["Chief Audit Executive", "CAE"]),
    ("AIL", ["AI Leader", "AIL"]),
    ("CDAO", ["CDAO"]),
    ("CSO", ["CSO"]),
    ("TCEO", ["Tech CEO", "TCEO"]),
    ("CPO GBS", ["CPO - Procurement (GBS)", "CPO - Procurement", "CPO - GBS", "CPO (GBS)", "CPO GBS"]),
    ("CPO HT", ["CPO - Product (HT)", "CPO - Product", "CPO - HT", "CPO (HT)", "CPO HT"]),
    ("CFO", ["CFO"]),
    ("GC", ["General Counsel", "GC"]),
    ("TSL", ["TSL", "Tech Services Leader", "Tech Service Leader"]),
    ("CISO", ["CISO"]),
]

# Role abbreviation mapping (for email filenames)
ROLE_ABBREVIATIONS = {
    "Chief Audit Executive": "CAE",
    "CPO - Procurement (GBS)": "CPO GBS",
    "CPO - Product (HT)": "CPO HT",
    "R&D": "RD",
    "Customer Service": "CS",
    "General Counsel": "GC",
    "Tech CEO": "TCEO",
    "Tech CMO": "TCMO",
    "AI Leader": "AIL",
    "Tech Services Leader": "TSL",
    "Tech Service Leader": "TSL",
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
