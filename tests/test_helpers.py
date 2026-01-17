"""Tests for helper utility functions."""
import pytest
from utils.helpers import (
    format_date,
    format_date_display,
    get_today_date,
    format_quantity,
    validate_file_exists,
    get_file_name
)


class TestFormatDate:
    """Tests for format_date function."""
    
    def test_format_valid_date(self):
        """Test formatting a valid date."""
        result = format_date("2024-01-15")
        assert result == "2024-01-15"
    
    def test_format_empty_date(self):
        """Test formatting an empty date."""
        result = format_date(None)
        assert result is None
    
    def test_format_invalid_date(self):
        """Test formatting an invalid date (returns as-is)."""
        result = format_date("invalid")
        assert result == "invalid"


class TestFormatDateDisplay:
    """Tests for format_date_display function."""
    
    def test_format_date_display(self):
        """Test formatting date for display."""
        result = format_date_display("2024-01-15")
        assert "Jan" in result
        assert "2024" in result
    
    def test_format_empty_date_display(self):
        """Test formatting empty date."""
        result = format_date_display(None)
        assert result == ""
    
    def test_format_invalid_date_display(self):
        """Test formatting invalid date (returns as-is)."""
        result = format_date_display("invalid")
        assert result == "invalid"


class TestGetTodayDate:
    """Tests for get_today_date function."""
    
    def test_get_today_date_format(self):
        """Test that today's date is in correct format."""
        result = get_today_date()
        assert len(result) == 10
        assert result.count('-') == 2
        # Should be YYYY-MM-DD format
        parts = result.split('-')
        assert len(parts) == 3
        assert len(parts[0]) == 4  # Year
        assert len(parts[1]) == 2  # Month
        assert len(parts[2]) == 2  # Day


class TestFormatQuantity:
    """Tests for format_quantity function."""
    
    def test_format_quantity_with_unit(self):
        """Test formatting quantity with unit."""
        result = format_quantity(10.5, "pieces")
        assert result == "10.5 pieces"
    
    def test_format_quantity_without_unit(self):
        """Test formatting quantity without unit."""
        result = format_quantity(10.5, None)
        assert result == "10.5"
    
    def test_format_none_quantity(self):
        """Test formatting None quantity."""
        result = format_quantity(None, "pieces")
        assert result == ""


class TestValidateFileExists:
    """Tests for validate_file_exists function."""
    
    def test_validate_nonexistent_file(self):
        """Test validating non-existent file."""
        result = validate_file_exists("/nonexistent/file/path.txt")
        assert result is False
    
    def test_validate_empty_path(self):
        """Test validating empty path."""
        result = validate_file_exists("")
        assert result is False


class TestGetFileName:
    """Tests for get_file_name function."""
    
    def test_get_file_name_from_path(self):
        """Test extracting filename from path."""
        result = get_file_name("/path/to/file.txt")
        assert result == "file.txt"
    
    def test_get_file_name_empty(self):
        """Test getting filename from empty path."""
        result = get_file_name("")
        assert result == ""
    
    def test_get_file_name_none(self):
        """Test getting filename from None."""
        result = get_file_name(None)
        assert result == ""

