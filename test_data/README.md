# Test Data for Manual Testing

This folder contains complex Word documents for manually testing the Insight Processor application.

## Files

### Input Files (`input/`)

| File | Description | Roles/Sections |
|------|-------------|----------------|
| `Weekly_Insights_Full.docx` | Complex insights document | 5 roles: CAE, GC, CPO-Procurement, Tech CEO, R&D |
| `Weekly_Insights_Simple.docx` | Simpler insights document | 2 roles: Customer Service, VP of Digital Innovation |
| `Email_Templates_Full.docx` | Email templates document | 5 roles with BD, AE, EP templates each |

### Output Folder (`output/`)

Empty folder ready to receive generated files.

## Test Scenarios

### Scenario 1: Full Workflow (Recommended First Test)

1. **Run the application:**
   ```bash
   cd "/Users/aaronhenckler/Documents/AI Projects/Insight Processor"
   python insight_processor.py
   ```

2. **Choose option `A` (Run All Steps)**

3. **When prompted for files/folders:**
   - Step 1 input: `test_data/input/Weekly_Insights_Full.docx`
   - Step 1 output: `test_data/output`
   - Step 4 input: `test_data/input/Email_Templates_Full.docx`
   - Step 4 target folder: `test_data/output`

4. **Verify results:**
   - 5 subfolders created (one per role)
   - Each subfolder has a renamed `.docx` file with date prefix
   - Files are formatted (Calibri 11pt, bold headers, bullets)
   - BD_AE and EP email files in each subfolder

### Scenario 2: Step-by-Step Testing

#### Step 1: Split Insights
- Input: `test_data/input/Weekly_Insights_Full.docx`
- Output: `test_data/output`
- **Expected:** 5 subfolders created, each with `{RoleName}.docx`

#### Step 2: Clean & Rename
- Input: `test_data/output` (after Step 1)
- **Expected:** Files renamed to `{date}_{role}_{title}.docx`
- Backups created with timestamp

#### Step 3: Format Insights
- Input: `test_data/output` (after Step 2)
- **Expected:**
  - All text set to Calibri 11pt
  - Headers bolded (Why This Matters, Implications, etc.)
  - Bullet points applied (numbered lists converted)
  - Intro lines NOT bulleted (lines ending with `:`)

#### Step 4: Split Emails
- Input: `test_data/input/Email_Templates_Full.docx`
- Target: `test_data/output` (must have subfolders from Step 1)
- **Expected:** BD_AE_emails.docx and EP_email.docx in each subfolder

### Scenario 3: Simple Test

Use `Weekly_Insights_Simple.docx` for a quicker test with only 2 roles:
- Customer Service (known abbreviation: CS)
- VP of Digital Innovation (unknown role - tests fallback sanitization)

## What to Verify

### After Step 1 (Split)
- [ ] Correct number of subfolders created
- [ ] Each subfolder named exactly like the Heading 2 text
- [ ] Each subfolder contains a `.docx` file
- [ ] Hyperlinks preserved in split files

### After Step 2 (Clean/Rename)
- [ ] First line deleted from each document
- [ ] Files renamed with date prefix (2 Mondays from today)
- [ ] Role abbreviations used (CAE, GC, etc.)
- [ ] Backup files created

### After Step 3 (Format)
- [ ] Font is Calibri 11pt throughout
- [ ] Headers are bold ("Why This Matters", "Implications", etc.)
- [ ] Spacing after title paragraph
- [ ] Numbered lists converted to dot bullets
- [ ] Dashed lists converted to dot bullets
- [ ] Intro lines NOT bulleted (text ending with `:`)

### After Step 4 (Email Split)
- [ ] BD_AE_emails.docx created in each role folder
- [ ] EP_email.docx created in each role folder
- [ ] Correct date prefix on email files
- [ ] Role abbreviations in email filenames

## Regenerating Test Files

If you need to regenerate the test files:

```bash
python test_data/create_test_files.py
```

This will overwrite existing files in `test_data/input/`.

## Cleaning Up

To reset for fresh testing:

```bash
rm -rf test_data/output/*
```

## Content Details

### Weekly_Insights_Full.docx

Each role section contains:
- Title of Insight
- Why This Matters (with intro line + numbered list)
- Implications
- Why Gartner (with hyperlinks)
- Visual/Graphic
- Engage Clients and Prospects
- Probing Questions (with intro line + various list formats)
- AskGartner Prompts to Recommend (with intro line + letter list)
- Insights to Engage (with hyperlinks)

**Challenge elements:**
- Hyperlinks to preserve
- Numbered lists: `1.`, `2.`, `3.`
- Letter lists: `a.`, `b.`, `c.`
- Parenthetical lists: `(1)`, `(2)`
- Dashed lists: `- item`
- Intro lines ending with `:`
- Content before first Heading 2 (should be ignored)

### Email_Templates_Full.docx

Each role has:
- SALES BUSINESS DEVELOPER PROSPECT EMAIL (BD)
- SALES ACCOUNT EXECUTIVE CLIENT EMAIL (AE)
- SERVICE EXECUTIVE PARTNER (EP)

5 roles = 15 email templates total
