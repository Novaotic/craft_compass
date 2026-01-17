"""Helper utility functions."""
from datetime import datetime
from typing import Optional
import os


def format_date(date_string: Optional[str], format_string: str = "%Y-%m-%d") -> Optional[str]:
    """
    Format a date string to a specific format.
    
    Args:
        date_string: Date string to format
        format_string: Target format (default: YYYY-MM-DD)
    
    Returns:
        Formatted date string or None if input is empty
    """
    if not date_string:
        return None
    
    try:
        # Try to parse and reformat
        dt = datetime.strptime(date_string, "%Y-%m-%d")
        return dt.strftime(format_string)
    except (ValueError, TypeError):
        return date_string  # Return as-is if parsing fails


def format_date_display(date_string: Optional[str]) -> str:
    """
    Format a date string for display (e.g., "Jan 1, 2024").
    
    Args:
        date_string: Date string in YYYY-MM-DD format
    
    Returns:
        Formatted date string for display
    """
    if not date_string:
        return ""
    
    try:
        dt = datetime.strptime(date_string, "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except (ValueError, TypeError):
        return date_string


def get_today_date() -> str:
    """
    Get today's date in YYYY-MM-DD format.
    
    Returns:
        Today's date as string
    """
    return datetime.now().strftime("%Y-%m-%d")


def format_quantity(quantity: Optional[float], unit: Optional[str] = None) -> str:
    """
    Format a quantity with its unit for display.
    
    Args:
        quantity: The quantity value
        unit: The unit (e.g., "grams", "meters")
    
    Returns:
        Formatted string like "5.0 grams" or "5.0"
    """
    if quantity is None:
        return ""
    
    if unit:
        return f"{quantity} {unit}"
    return str(quantity)


def validate_file_exists(file_path: str) -> bool:
    """
    Check if a file exists.
    
    Args:
        file_path: Path to the file
    
    Returns:
        True if file exists, False otherwise
    """
    return os.path.isfile(file_path) if file_path else False


def get_file_name(file_path: Optional[str]) -> str:
    """
    Extract just the filename from a full path.
    
    Args:
        file_path: Full path to file
    
    Returns:
        Just the filename or empty string
    """
    if not file_path:
        return ""
    return os.path.basename(file_path)

