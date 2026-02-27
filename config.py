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

# Role folder definitions: (create_name, full_name, [all_synonyms])
# - create_name: the folder name to create if none exists
# - full_name: the full display name used for CXO replacement
# - all_synonyms: all variations of the role name (for input matching AND folder searching)
# Matching is case-insensitive and exact (not substring)
ROLE_FOLDER_DEFINITIONS = [
    ("CIO",      "Chief Information Officer",         ["CIO"]),
    ("TCMO",     "Tech CMO",                          ["Tech CMO", "TCMO"]),
    ("CHRO",     "Chief Human Resources Officer",     ["CHRO"]),
    ("CSCO",     "Chief Supply Chain Officer",        ["CSCO"]),
    ("CMO",      "Chief Marketing Officer",           ["CMO"]),
    ("CS",       "Customer Service Leader",           ["Customer Service", "CS"]),
    ("RD",       "R&D Leader",                        ["R&D", "RND", "RD"]),
    ("CAE",      "Chief Audit Executive",             ["Chief Audit Executive", "CAE"]),
    ("AIL",      "AI Leader",                         ["AI Leader", "AIL"]),
    ("CDAO",     "Chief Data and Analytics Officer",  ["CDAO"]),
    ("CSO",      "Chief Sales Officer",               ["CSO"]),
    ("TCEO",     "Tech CEO",                          ["Tech CEO", "TCEO"]),
    ("CPO GBS",  "Chief Procurement Officer",         ["CPO - Procurement (GBS)", "CPO - Procurement", "CPO - GBS", "CPO (GBS)", "CPO GBS"]),
    ("CPO HT",   "Chief Product Officer",             ["CPO - Product (HT)", "CPO - Product", "CPO - HT", "CPO (HT)", "CPO HT"]),
    ("CFO",      "Chief Financial Officer",           ["CFO"]),
    ("GC",       "General Counsel",                   ["General Counsel", "GC"]),
    ("TSL",      "Tech Services Leader",              ["TSL", "Tech Services Leader", "Tech Service Leader"]),
    ("CISO",     "Chief Information Security Officer",["CISO"]),
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

# EP email hyperlink tag (appended to all hyperlinks in generated EP emails)
EP_URL_SUFFIX = "?ref=salesenablementnewsletter"

# AskGartner prompt hyperlink base URL
ASKGARTNER_BASE_URL = "https://www.gartner.com/askgartner?q="

# AskGartner section header name (used to identify the section for hyperlink conversion)
ASKGARTNER_HEADER = "AskGartner Prompts to Recommend"

# Email template heading patterns
EMAIL_HEADING_PATTERNS = {
    "BD": ["SALES BUSINESS DEVELOPER", "PROSPECT EMAIL"],
    "AE": ["SALES ACCOUNT EXECUTIVE", "CLIENT EMAIL"],
    "EP": ["SERVICE EXECUTIVE PARTNER", "CLIENT EMAIL"],
}
