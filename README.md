# Insight Processor

A unified pipeline tool for processing Word documents. Combines four document processing operations into a single interactive application.

## Features

### Step 1: Split Insights
- Splits a Word document into separate files based on Heading 2 sections
- Creates job-role subfolders automatically
- Preserves all hyperlinks using relationship mapping

### Step 2: Clean/Rename Files
- Deletes the first line of each document
- Extracts the 3rd line for the new filename
- Renames files to: `[MM.DD]_[subfolder]_[3rd line].docx`
- Date is calculated as 2 Mondays from today
- Creates backups before modifying files

### Step 3: Format Insights
- Sets font to Calibri 11pt throughout
- Bolds specific section headers
- Converts content to bullet points in designated sections
- Skips intro lines (lines ending with `:` or full sentences)
- Preserves all hyperlinks

### Step 4: Split Emails
- Splits email templates by job role
- Creates `BD_AE_emails.docx` and `EP_email.docx` per role
- Applies Calibri 11pt formatting

## Installation

1. Ensure Python 3.8+ is installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script:

```bash
python insight_processor.py
```

### Interactive Menu

```
========================================
       INSIGHT PROCESSOR
========================================

Select steps to run:
  [1] Split Insights        (from insights doc)
  [2] Clean/Rename Files    (rename split files)
  [3] Format Insights       (apply formatting)
  [4] Split Emails          (from emails doc)
  [A] Run ALL steps
  [Q] Quit

Enter selection (e.g., 1,2,3 or A):
```

You can run individual steps, multiple steps (e.g., `1,2,3`), or all steps at once.

## Project Structure

```
Insight Processor/
├── insight_processor.py      # Main entry point with interactive UI
├── config.py                 # Configuration constants
├── utils/
│   ├── __init__.py
│   ├── date_utils.py         # Monday calculations
│   ├── file_utils.py         # File discovery, backup, validation
│   ├── folder_utils.py       # Folder creation, matching
│   ├── paragraph_utils.py    # Copy paragraphs with hyperlinks
│   ├── text_utils.py         # Filename sanitization, role abbreviations
│   └── formatting_utils.py   # Font, bullet, header formatting
├── processors/
│   ├── __init__.py
│   ├── insight_splitter.py   # Step 1: Split insights by Heading 2
│   ├── file_cleaner.py       # Step 2: Clean/rename insight files
│   ├── insight_formatter.py  # Step 3: Format insight files
│   └── email_splitter.py     # Step 4: Split email templates
├── qc/
│   ├── __init__.py
│   └── validators.py         # QC checks (headings, content)
├── requirements.txt
└── README.md
```

## Configuration

Edit `config.py` to customize:

### Headers to Bold
```python
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
```

### Sections to Convert to Bullets
```python
BULLET_SECTIONS = [
    ("Why This Matters", "Implications"),
    ("Probing Questions", "AskGartner Prompts to Recommend"),
    ("AskGartner Prompts to Recommend", None),
]
```

### Role Abbreviations
```python
ROLE_ABBREVIATIONS = {
    "Chief Audit Executive": "CAE",
    "CPO - Procurement (GBS)": "CPO_GBS",
    "CPO - Product (HT)": "CPO_GTS",
    "R&D": "RD",
    "Customer Service": "CS",
    "General Counsel": "GC",
    "Tech CEO": "TCEO",
}
```

## QC Validation

The tool performs automatic validation:

### Pre-Processing
- Verifies documents open successfully
- Checks for required Heading 2 sections
- Validates email template structure

### Post-Processing
- Verifies expected files were created
- Checks formatting was applied correctly
- Validates hyperlinks are preserved

The pipeline stops on critical validation failures.

## File Conflict Handling

When a target file already exists:
1. A backup is created: `{filename}_backup_{YYYYMMDD_HHMMSS}.docx`
2. The existing file is overwritten
3. Backup location is logged in the summary

## Dependencies

- `python-docx>=0.8.11`

## Example Output

```
Step 1: Split Insights
----------------------------------------
  [QC] Validating insights document... OK
  Found 12 Heading 2 sections
  Creating/using subfolder: Chief Audit Executive
  Created: Chief Audit Executive.docx
  ...

========================================
           SUMMARY
========================================
Steps completed: 4/4
Files created: 24
Files renamed: 12
Files formatted: 12
Warnings: 0
Errors: 0

Output directory: /path/to/output
========================================
```
