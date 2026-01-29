"""
Date utility functions for calculating Monday dates.
"""

from datetime import datetime, timedelta


def get_next_monday(from_date: datetime) -> datetime:
    """
    Get the next Monday from the given date.

    Args:
        from_date: The date to start from

    Returns:
        The next Monday as a datetime object
    """
    days_ahead = 0 - from_date.weekday()  # Monday is 0
    if days_ahead <= 0:  # Target day already happened this week or is today
        days_ahead += 7
    return from_date + timedelta(days=days_ahead)


def get_two_mondays_from_now() -> datetime:
    """
    Calculate the date that is 2 Mondays from today.

    Returns:
        The second Monday from today as a datetime object
    """
    today = datetime.now()
    first_monday = get_next_monday(today)
    second_monday = get_next_monday(first_monday + timedelta(days=1))
    return second_monday


def format_date_for_filename(date: datetime) -> str:
    """
    Format a date for use in filenames.

    Args:
        date: The datetime to format

    Returns:
        String in "MM.DD" format (e.g., "2.3" for February 3rd)
    """
    return f"{date.month}.{date.day}"
