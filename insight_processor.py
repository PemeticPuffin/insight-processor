#!/usr/bin/env python3
"""
Insight Processor - Unified Pipeline Tool

Combines four Word document processing operations:
1. Split Insights - Split documents by Heading 2
2. Clean/Rename Files - Delete first line, rename based on 3rd line
3. Format Insights - Apply Calibri 11pt, bold headers, bullets
4. Split Emails - Split email templates by job role
"""

import sys
from pathlib import Path
from typing import List, Optional, Tuple

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from processors.insight_splitter import split_insights, get_heading_list
from processors.file_cleaner import clean_and_rename_files
from processors.insight_formatter import format_insights
from processors.email_splitter import split_emails
from qc.validators import (
    validate_insights_document,
    validate_emails_document,
    validate_split_files,
    validate_formatting,
)
from utils.file_utils import validate_docx


class InsightProcessor:
    """Main application class for the Insight Processor pipeline."""

    def __init__(self):
        self.insights_path: Optional[Path] = None
        self.emails_path: Optional[Path] = None
        self.output_dir: Optional[Path] = None
        self.messages: List[str] = []

        # Statistics
        self.stats = {
            'files_created': 0,
            'files_renamed': 0,
            'files_formatted': 0,
            'warnings': 0,
            'errors': 0,
            'steps_completed': 0,
            'steps_total': 0,
        }

    def log(self, message: str):
        """Log a message and print it."""
        self.messages.append(message)
        print(message)

    def display_header(self):
        """Display the application header."""
        print("\n" + "=" * 48)
        print("           INSIGHT PROCESSOR")
        print("=" * 48)

    def display_menu(self) -> str:
        """Display the main menu and get user selection."""
        print("\nSelect steps to run:")
        print("  [1] Split Insights        (from insights doc)")
        print("  [2] Clean/Rename Files    (rename split files)")
        print("  [3] Format Insights       (apply formatting)")
        print("  [4] Split Emails          (from emails doc)")
        print("  [A] Run ALL steps")
        print("  [Q] Quit")
        print()

        selection = input("Enter selection (e.g., 1,2,3 or A): ").strip().upper()
        return selection

    def get_file_path(self, prompt: str, required: bool = True) -> Optional[Path]:
        """Get a file path from user input."""
        while True:
            path_str = input(prompt).strip()

            if not path_str:
                if required:
                    print("  Path is required. Please enter a valid path.")
                    continue
                return None

            # Handle quotes
            path_str = path_str.strip('"').strip("'")

            path = Path(path_str).expanduser().resolve()

            if not path.exists():
                print(f"  File not found: {path}")
                continue

            if not path.suffix.lower() == '.docx':
                print("  File must be a .docx file.")
                continue

            if not validate_docx(path):
                print("  Invalid Word document. Please check the file.")
                continue

            return path

    def get_directory_path(self, prompt: str) -> Optional[Path]:
        """Get a directory path from user input."""
        while True:
            path_str = input(prompt).strip()

            if not path_str:
                print("  Path is required. Please enter a valid path.")
                continue

            # Handle quotes
            path_str = path_str.strip('"').strip("'")

            path = Path(path_str).expanduser().resolve()

            # Create directory if it doesn't exist
            if not path.exists():
                create = input(f"  Directory does not exist. Create it? (y/n): ").strip().lower()
                if create == 'y':
                    path.mkdir(parents=True, exist_ok=True)
                    print(f"  Created: {path}")
                else:
                    continue

            if not path.is_dir():
                print("  Path must be a directory.")
                continue

            return path

    def run_step1_split_insights(self) -> bool:
        """Step 1: Split insights document by Heading 2."""
        self.log("\nStep 1: Split Insights")
        self.log("-" * 40)

        if not self.insights_path:
            self.log("  [ERROR] Insights document path not set")
            self.stats['errors'] += 1
            return False

        # Validate document
        self.log("  [QC] Validating insights document...")
        success, messages = validate_insights_document(self.insights_path)

        for msg in messages:
            self.log(f"    {msg}")

        if not success:
            self.log("  [ERROR] Validation failed. Stopping.")
            self.stats['errors'] += 1
            return False

        self.log("  [QC] Validation OK")

        # Split the document
        files_created, sections_found, created_files = split_insights(
            self.insights_path,
            self.output_dir,
            create_subfolders=True,
            progress_callback=lambda m: self.log(f"  {m}")
        )

        self.stats['files_created'] += files_created
        self.log(f"\n  Created {files_created} files in {files_created} subfolders")

        return files_created > 0

    def run_step2_clean_rename(self) -> bool:
        """Step 2: Clean and rename split files."""
        self.log("\nStep 2: Clean/Rename Files")
        self.log("-" * 40)

        processed, skipped, backups = clean_and_rename_files(
            self.output_dir,
            progress_callback=lambda m: self.log(f"  {m}")
        )

        self.stats['files_renamed'] += processed

        if skipped > 0:
            self.stats['warnings'] += skipped

        self.log(f"\n  Processed: {processed}, Skipped: {skipped}")

        return processed > 0 or skipped > 0

    def run_step3_format_insights(self) -> bool:
        """Step 3: Format insight files."""
        self.log("\nStep 3: Format Insights")
        self.log("-" * 40)

        success_count, failure_count = format_insights(
            self.output_dir,
            recursive=True,
            progress_callback=lambda m: self.log(f"  {m}")
        )

        self.stats['files_formatted'] += success_count
        self.stats['errors'] += failure_count

        self.log(f"\n  Formatted: {success_count}, Failed: {failure_count}")

        return success_count > 0

    def run_step4_split_emails(self) -> bool:
        """Step 4: Split email templates."""
        self.log("\nStep 4: Split Emails")
        self.log("-" * 40)

        if not self.emails_path:
            self.log("  [SKIP] No emails document provided")
            return True

        # Validate document
        self.log("  [QC] Validating emails document...")
        success, messages = validate_emails_document(self.emails_path)

        for msg in messages:
            self.log(f"    {msg}")

        if not success:
            self.log("  [ERROR] Validation failed. Stopping.")
            self.stats['errors'] += 1
            return False

        self.log("  [QC] Validation OK")

        # Split emails
        processed, skipped, created_files = split_emails(
            self.emails_path,
            self.output_dir,
            progress_callback=lambda m: self.log(f"  {m}")
        )

        self.stats['files_created'] += len(created_files)

        self.log(f"\n  Jobs processed: {processed}, Skipped: {skipped}")

        return processed > 0

    def display_summary(self, steps_run: List[int]):
        """Display the final summary."""
        print("\n" + "=" * 48)
        print("               SUMMARY")
        print("=" * 48)

        steps_completed = len([s for s in steps_run if s])
        print(f"Steps completed: {steps_completed}/{self.stats['steps_total']}")
        print(f"Files created: {self.stats['files_created']}")
        print(f"Files renamed: {self.stats['files_renamed']}")
        print(f"Files formatted: {self.stats['files_formatted']}")
        print(f"Warnings: {self.stats['warnings']}")
        print(f"Errors: {self.stats['errors']}")
        print()
        print(f"Output directory: {self.output_dir}")
        print("=" * 48)

    def parse_selection(self, selection: str) -> List[int]:
        """Parse user selection into list of step numbers."""
        if selection == 'A':
            return [1, 2, 3, 4]
        elif selection == 'Q':
            return []

        steps = []
        for part in selection.replace(' ', '').split(','):
            try:
                step = int(part)
                if 1 <= step <= 4:
                    steps.append(step)
            except ValueError:
                pass

        return sorted(set(steps))

    def run(self):
        """Main application loop."""
        self.display_header()

        # Get selection
        selection = self.display_menu()
        steps = self.parse_selection(selection)

        if not steps:
            print("\nExiting. Goodbye!")
            return

        self.stats['steps_total'] = len(steps)

        # Get required paths based on steps
        print("\n--- Input Paths ---")

        if 1 in steps:
            self.insights_path = self.get_file_path(
                "Enter path to insights document: ",
                required=True
            )

        if 4 in steps:
            self.emails_path = self.get_file_path(
                "Enter path to email templates document (or press Enter to skip): ",
                required=False
            )

        self.output_dir = self.get_directory_path(
            "Enter output directory: "
        )

        if not self.output_dir:
            print("\nOutput directory is required. Exiting.")
            return

        # Run selected steps
        print("\n--- Processing ---")
        results = []

        step_functions = {
            1: self.run_step1_split_insights,
            2: self.run_step2_clean_rename,
            3: self.run_step3_format_insights,
            4: self.run_step4_split_emails,
        }

        for step in steps:
            if step in step_functions:
                success = step_functions[step]()
                results.append(success)

                if not success and step in [1]:  # Critical steps
                    self.log(f"\n[PIPELINE STOPPED] Step {step} failed critically.")
                    break

        # Display summary
        self.display_summary(results)


def main():
    """Entry point for the application."""
    try:
        app = InsightProcessor()
        app.run()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
