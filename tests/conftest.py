"""Pytest configuration and fixtures."""
import pytest
import os
import tempfile
import shutil
from database.database import CraftCompassDB


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test_craft_compass.db")
    
    # Create database instance
    db = CraftCompassDB(db_path=db_path)
    db.initialize()
    
    yield db
    
    # Cleanup: remove temporary directory
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_supplier():
    """Create a sample supplier dictionary."""
    return {
        'name': 'Test Supplier',
        'contact_info': 'test@example.com',
        'website': 'https://example.com',
        'notes': 'Test notes'
    }


@pytest.fixture
def sample_item():
    """Create a sample item dictionary."""
    return {
        'name': 'Test Item',
        'category': 'Electronics',
        'quantity': 10.0,
        'unit': 'pieces',
        'supplier_id': None,
        'purchase_date': '2024-01-15',
        'photo_path': None
    }


@pytest.fixture
def sample_project():
    """Create a sample project dictionary."""
    return {
        'name': 'Test Project',
        'description': 'A test project',
        'date_created': '2024-01-20'
    }

