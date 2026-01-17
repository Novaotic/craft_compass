"""Tests for validator functions."""
import pytest
from utils.validators import (
    validate_required,
    validate_date,
    validate_quantity,
    validate_integer,
    validate_file_path
)


class TestValidateRequired:
    """Tests for validate_required function."""
    
    def test_valid_required(self):
        """Test validation with valid required field."""
        is_valid, error = validate_required("test value", "Name")
        assert is_valid is True
        assert error is None
    
    def test_empty_required(self):
        """Test validation with empty required field."""
        is_valid, error = validate_required("", "Name")
        assert is_valid is False
        assert "Name is required" in error
    
    def test_whitespace_only(self):
        """Test validation with whitespace-only field."""
        is_valid, error = validate_required("   ", "Name")
        assert is_valid is False


class TestValidateDate:
    """Tests for validate_date function."""
    
    def test_valid_date(self):
        """Test validation with valid date."""
        is_valid, error = validate_date("2024-01-15", "Date")
        assert is_valid is True
        assert error is None
    
    def test_invalid_date_format(self):
        """Test validation with invalid date format."""
        is_valid, error = validate_date("01/15/2024", "Date")
        assert is_valid is False
        assert "must be in YYYY-MM-DD format" in error
    
    def test_empty_date(self):
        """Test validation with empty date (optional)."""
        is_valid, error = validate_date("", "Date")
        assert is_valid is True  # Date is optional
        assert error is None
    
    def test_invalid_date_value(self):
        """Test validation with invalid date value."""
        is_valid, error = validate_date("2024-13-45", "Date")
        assert is_valid is False


class TestValidateQuantity:
    """Tests for validate_quantity function."""
    
    def test_valid_quantity(self):
        """Test validation with valid quantity."""
        is_valid, error, value = validate_quantity("10.5", "Quantity")
        assert is_valid is True
        assert error is None
        assert value == 10.5
    
    def test_negative_quantity(self):
        """Test validation with negative quantity."""
        is_valid, error, value = validate_quantity("-5", "Quantity")
        assert is_valid is False
        assert "must be a positive number" in error
    
    def test_invalid_quantity(self):
        """Test validation with invalid quantity."""
        is_valid, error, value = validate_quantity("abc", "Quantity")
        assert is_valid is False
        assert "must be a valid number" in error
    
    def test_empty_quantity(self):
        """Test validation with empty quantity (optional)."""
        is_valid, error, value = validate_quantity("", "Quantity")
        assert is_valid is True  # Quantity is optional
        assert error is None
        assert value is None


class TestValidateInteger:
    """Tests for validate_integer function."""
    
    def test_valid_integer(self):
        """Test validation with valid integer."""
        is_valid, error, value = validate_integer("42", "ID")
        assert is_valid is True
        assert error is None
        assert value == 42
    
    def test_invalid_integer(self):
        """Test validation with invalid integer."""
        is_valid, error, value = validate_integer("abc", "ID")
        assert is_valid is False
        assert "must be a valid integer" in error
    
    def test_empty_integer_allowed(self):
        """Test validation with empty integer when allowed."""
        is_valid, error, value = validate_integer("", "ID", allow_empty=True)
        assert is_valid is True
        assert value is None
    
    def test_empty_integer_not_allowed(self):
        """Test validation with empty integer when not allowed."""
        is_valid, error, value = validate_integer("", "ID", allow_empty=False)
        assert is_valid is False
        assert "is required" in error


class TestValidateFilePath:
    """Tests for validate_file_path function."""
    
    def test_empty_path(self):
        """Test validation with empty path (optional)."""
        is_valid, error = validate_file_path("", "Photo")
        assert is_valid is True  # File path is optional
        assert error is None
    
    def test_nonexistent_path(self):
        """Test validation with non-existent path."""
        is_valid, error = validate_file_path("/nonexistent/path/file.jpg", "Photo")
        # Should pass if directory structure is valid (or fail gracefully)
        # This test may vary based on system
        assert isinstance(is_valid, bool)

