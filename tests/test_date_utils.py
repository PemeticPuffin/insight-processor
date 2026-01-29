"""
Tests for date_utils.py

These tests challenge the date calculation logic with edge cases including:
- All days of the week
- Year boundaries
- Leap years
- Month boundaries
- Various date formats
"""

import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.date_utils import get_next_monday, get_two_mondays_from_now, format_date_for_filename


class TestGetNextMonday:
    """Tests for get_next_monday function."""

    @pytest.mark.parametrize("weekday,days_until_monday", [
        (0, 7),  # Monday -> next Monday (7 days)
        (1, 6),  # Tuesday -> next Monday (6 days)
        (2, 5),  # Wednesday -> next Monday (5 days)
        (3, 4),  # Thursday -> next Monday (4 days)
        (4, 3),  # Friday -> next Monday (3 days)
        (5, 2),  # Saturday -> next Monday (2 days)
        (6, 1),  # Sunday -> next Monday (1 day)
    ])
    def test_next_monday_from_each_day_of_week(self, weekday, days_until_monday):
        """Test that we correctly calculate next Monday from each day of week."""
        # Find a date with the desired weekday in January 2024
        base_date = datetime(2024, 1, 1)  # This is a Monday
        test_date = base_date + timedelta(days=weekday)

        result = get_next_monday(test_date)

        assert result.weekday() == 0  # Result should be a Monday
        assert result > test_date  # Result should be after input date
        assert (result - test_date).days == days_until_monday

    def test_monday_gives_next_monday_not_same_day(self):
        """If input is Monday, should return NEXT Monday, not same day."""
        monday = datetime(2024, 1, 1)  # Known Monday
        result = get_next_monday(monday)

        assert result == datetime(2024, 1, 8)
        assert result != monday

    def test_year_boundary_crossing(self):
        """Test Monday calculation when crossing into new year."""
        # December 31, 2024 is a Tuesday
        dec_31 = datetime(2024, 12, 31)
        result = get_next_monday(dec_31)

        assert result.year == 2025
        assert result.month == 1
        assert result.weekday() == 0

    def test_leap_year_february(self):
        """Test Monday calculation around leap year February 29."""
        # February 29, 2024 is a Thursday (2024 is a leap year)
        leap_day = datetime(2024, 2, 29)
        result = get_next_monday(leap_day)

        assert result == datetime(2024, 3, 4)
        assert result.weekday() == 0

    def test_non_leap_year_february(self):
        """Test Monday calculation around February 28 in non-leap year."""
        # February 28, 2023 is a Tuesday (2023 is not a leap year)
        feb_28 = datetime(2023, 2, 28)
        result = get_next_monday(feb_28)

        assert result == datetime(2023, 3, 6)
        assert result.weekday() == 0

    def test_end_of_month_boundary(self):
        """Test Monday calculation at end of various months."""
        test_cases = [
            (datetime(2024, 1, 31), datetime(2024, 2, 5)),   # Jan 31 Wed -> Feb 5
            (datetime(2024, 4, 30), datetime(2024, 5, 6)),   # Apr 30 Tue -> May 6
            (datetime(2024, 6, 30), datetime(2024, 7, 1)),   # Jun 30 Sun -> Jul 1
            (datetime(2024, 9, 30), datetime(2024, 10, 7)),  # Sep 30 Mon -> Oct 7
        ]

        for input_date, expected_monday in test_cases:
            result = get_next_monday(input_date)
            assert result == expected_monday, f"Failed for {input_date}"

    def test_preserves_time_component(self):
        """Test that time component is preserved (not reset to midnight)."""
        date_with_time = datetime(2024, 1, 3, 14, 30, 45)  # Wednesday 2:30:45 PM
        result = get_next_monday(date_with_time)

        assert result.hour == 14
        assert result.minute == 30
        assert result.second == 45

    def test_distant_future_date(self):
        """Test with a date far in the future."""
        future_date = datetime(2099, 6, 15)  # Far future
        result = get_next_monday(future_date)

        assert result > future_date
        assert result.weekday() == 0

    def test_very_old_date(self):
        """Test with historical dates."""
        old_date = datetime(1900, 1, 1)  # January 1, 1900 was a Monday
        result = get_next_monday(old_date)

        assert result == datetime(1900, 1, 8)
        assert result.weekday() == 0


class TestGetTwoMondaysFromNow:
    """Tests for get_two_mondays_from_now function."""

    @freeze_time("2024-01-01")  # Monday
    def test_from_monday(self):
        """Two Mondays from a Monday should be 14 days later."""
        result = get_two_mondays_from_now()

        assert result == datetime(2024, 1, 15)
        assert result.weekday() == 0

    @freeze_time("2024-01-02")  # Tuesday
    def test_from_tuesday(self):
        """Two Mondays from Tuesday."""
        result = get_two_mondays_from_now()

        # First Monday: Jan 8, Second Monday: Jan 15
        assert result == datetime(2024, 1, 15)
        assert result.weekday() == 0

    @freeze_time("2024-01-05")  # Friday
    def test_from_friday(self):
        """Two Mondays from Friday."""
        result = get_two_mondays_from_now()

        # First Monday: Jan 8, Second Monday: Jan 15
        assert result == datetime(2024, 1, 15)
        assert result.weekday() == 0

    @freeze_time("2024-01-07")  # Sunday
    def test_from_sunday(self):
        """Two Mondays from Sunday."""
        result = get_two_mondays_from_now()

        # First Monday: Jan 8, Second Monday: Jan 15
        assert result == datetime(2024, 1, 15)
        assert result.weekday() == 0

    @freeze_time("2024-12-28")  # Saturday
    def test_year_boundary(self):
        """Test two Mondays from now crossing year boundary."""
        result = get_two_mondays_from_now()

        # First Monday: Dec 30, 2024, Second Monday: Jan 6, 2025
        assert result.year == 2025
        assert result.month == 1
        assert result.weekday() == 0

    @freeze_time("2024-02-26")  # Monday before leap day
    def test_leap_year_crossing(self):
        """Test two Mondays calculation crossing leap day."""
        result = get_two_mondays_from_now()

        # First Monday: Mar 4, Second Monday: Mar 11
        assert result == datetime(2024, 3, 11)
        assert result.weekday() == 0

    @freeze_time("2023-02-20")  # Monday in non-leap year
    def test_non_leap_year_february(self):
        """Test in non-leap year February."""
        result = get_two_mondays_from_now()

        # First Monday: Feb 27, Second Monday: Mar 6
        assert result == datetime(2023, 3, 6)
        assert result.weekday() == 0


class TestFormatDateForFilename:
    """Tests for format_date_for_filename function."""

    @pytest.mark.parametrize("date,expected", [
        (datetime(2024, 1, 1), "1.1"),
        (datetime(2024, 1, 15), "1.15"),
        (datetime(2024, 2, 3), "2.3"),
        (datetime(2024, 12, 31), "12.31"),
        (datetime(2024, 10, 5), "10.5"),
        (datetime(2024, 6, 20), "6.20"),
    ])
    def test_basic_formatting(self, date, expected):
        """Test basic date formatting without leading zeros."""
        result = format_date_for_filename(date)
        assert result == expected

    def test_no_leading_zeros_on_month(self):
        """Verify single-digit months don't have leading zeros."""
        date = datetime(2024, 3, 15)
        result = format_date_for_filename(date)

        assert result == "3.15"
        assert not result.startswith("0")

    def test_no_leading_zeros_on_day(self):
        """Verify single-digit days don't have leading zeros."""
        date = datetime(2024, 11, 5)
        result = format_date_for_filename(date)

        assert result == "11.5"
        assert not result.endswith("05")

    def test_double_digit_month_and_day(self):
        """Test with double-digit month and day."""
        date = datetime(2024, 12, 25)
        result = format_date_for_filename(date)

        assert result == "12.25"

    def test_single_digit_month_and_day(self):
        """Test with single-digit month and day."""
        date = datetime(2024, 1, 1)
        result = format_date_for_filename(date)

        assert result == "1.1"

    def test_all_months(self):
        """Test formatting for each month of the year."""
        for month in range(1, 13):
            date = datetime(2024, month, 15)
            result = format_date_for_filename(date)

            assert result == f"{month}.15"
            assert "." in result

    def test_all_days(self):
        """Test formatting for each day of January (31 days)."""
        for day in range(1, 32):
            date = datetime(2024, 1, day)
            result = format_date_for_filename(date)

            assert result == f"1.{day}"

    def test_leap_day(self):
        """Test formatting February 29 in leap year."""
        date = datetime(2024, 2, 29)
        result = format_date_for_filename(date)

        assert result == "2.29"

    def test_ignores_year(self):
        """Verify that year is not included in the output."""
        date = datetime(2024, 5, 10)
        result = format_date_for_filename(date)

        assert "2024" not in result
        assert result == "5.10"

    def test_ignores_time_component(self):
        """Verify that time component doesn't affect output."""
        date_midnight = datetime(2024, 5, 10, 0, 0, 0)
        date_noon = datetime(2024, 5, 10, 12, 0, 0)
        date_evening = datetime(2024, 5, 10, 23, 59, 59)

        assert format_date_for_filename(date_midnight) == "5.10"
        assert format_date_for_filename(date_noon) == "5.10"
        assert format_date_for_filename(date_evening) == "5.10"


class TestDateUtilsIntegration:
    """Integration tests combining multiple date utility functions."""

    @freeze_time("2024-01-15")  # Monday
    def test_full_workflow(self):
        """Test the complete date calculation workflow."""
        # Get two Mondays from now
        target_date = get_two_mondays_from_now()

        # Format for filename
        date_str = format_date_for_filename(target_date)

        assert target_date == datetime(2024, 1, 29)
        assert date_str == "1.29"

    @freeze_time("2024-12-25")  # Wednesday near year end
    def test_year_end_workflow(self):
        """Test workflow near end of year."""
        target_date = get_two_mondays_from_now()
        date_str = format_date_for_filename(target_date)

        # First Monday: Dec 30, Second Monday: Jan 6, 2025
        assert target_date.year == 2025
        assert date_str == "1.6"

    @pytest.mark.parametrize("frozen_date,expected_str", [
        ("2024-03-01", "3.11"),   # March 1 (Fri) -> Mar 4 + Mar 11
        ("2024-06-15", "6.24"),   # Mid-June (Saturday) -> Jun 17 + Jun 24
        ("2024-09-01", "9.9"),    # September 1 (Sun) -> Sep 2 + Sep 9
        ("2024-11-11", "11.25"),  # Veterans Day (Monday) -> Nov 18 + Nov 25
    ])
    def test_various_start_dates(self, frozen_date, expected_str):
        """Test workflow from various starting dates."""
        with freeze_time(frozen_date):
            target_date = get_two_mondays_from_now()
            date_str = format_date_for_filename(target_date)

            assert date_str == expected_str
