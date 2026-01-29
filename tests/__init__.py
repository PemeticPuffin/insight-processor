"""
Tests for Insight Processor

This package contains comprehensive test suites for all modules:

- test_date_utils.py: Date calculation tests (Monday calculations, year boundaries)
- test_text_utils.py: Filename sanitization and role abbreviation tests
- test_file_utils.py: File operations (backup, discovery, validation)
- test_folder_utils.py: Folder creation and matching tests
- test_formatting_utils.py: Word document formatting tests
- test_insight_splitter.py: Document splitting by Heading 2
- test_file_cleaner.py: File cleaning and renaming tests
- test_insight_formatter.py: Document formatting application
- test_email_splitter.py: Email template splitting tests
- test_validators.py: QC validation tests

Run tests with:
    pytest                          # Run all tests
    pytest -v                       # Verbose output
    pytest tests/test_date_utils.py # Run specific test file
    pytest -k "monday"              # Run tests matching pattern
    pytest --cov=.                  # Run with coverage report
"""
