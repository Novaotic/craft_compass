"""Validation functions for user input."""
from datetime import datetime
from typing import Optional, Tuple


def validate_required(value: str, field_name: str = "Field") -> Tuple[bool, Optional[str]]:
    """
    Validate that a required field is not empty.
    
    Args:
        value: The value to validate
        field_name: Name of the field for error messages
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value or not str(value).strip():
        return False, f"{field_name} is required"
    return True, None


def validate_date(date_string: str, field_name: str = "Date") -> Tuple[bool, Optional[str]]:
    """
    Validate a date string in YYYY-MM-DD format.
    
    Args:
        date_string: Date string to validate
        field_name: Name of the field for error messages
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not date_string or not date_string.strip():
        return True, None  # Date is optional
    
    try:
        datetime.strptime(date_string.strip(), "%Y-%m-%d")
        return True, None
    except ValueError:
        return False, f"{field_name} must be in YYYY-MM-DD format"


def validate_quantity(quantity: str, field_name: str = "Quantity") -> Tuple[bool, Optional[str], Optional[float]]:
    """
    Validate a quantity value (must be a positive number).
    
    Args:
        quantity: Quantity string to validate
        field_name: Name of the field for error messages
    
    Returns:
        Tuple of (is_valid, error_message, parsed_value)
    """
    if not quantity or not str(quantity).strip():
        return True, None, None  # Quantity is optional
    
    try:
        qty_value = float(quantity)
        if qty_value < 0:
            return False, f"{field_name} must be a positive number", None
        return True, None, qty_value
    except ValueError:
        return False, f"{field_name} must be a valid number", None


def validate_integer(value: str, field_name: str = "Field", allow_empty: bool = True) -> Tuple[bool, Optional[str], Optional[int]]:
    """
    Validate an integer value.
    
    Args:
        value: Integer string to validate
        field_name: Name of the field for error messages
        allow_empty: Whether empty values are allowed
    
    Returns:
        Tuple of (is_valid, error_message, parsed_value)
    """
    if not value or not str(value).strip():
        if allow_empty:
            return True, None, None
        return False, f"{field_name} is required", None
    
    try:
        int_value = int(value)
        return True, None, int_value
    except ValueError:
        return False, f"{field_name} must be a valid integer", None


def validate_file_path(file_path: str, field_name: str = "File path") -> Tuple[bool, Optional[str]]:
    """
    Validate a file path (check if file exists, but allow empty).
    
    Args:
        file_path: File path to validate
        field_name: Name of the field for error messages
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file_path or not file_path.strip():
        return True, None  # File path is optional
    
    import os
    path = file_path.strip()
    if os.path.isfile(path):
        return True, None
    elif os.path.isdir(os.path.dirname(path)) if os.path.dirname(path) else True:
        # Directory exists, file might be created later
        return True, None
    else:
        return False, f"{field_name}: Directory does not exist"

