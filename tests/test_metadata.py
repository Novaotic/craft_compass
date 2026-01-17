"""Tests for metadata CRUD operations."""
import pytest
from database.database import CraftCompassDB
from controllers.item_controllers import ItemController


def test_add_metadata(temp_db):
    """Test adding metadata to an item."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create item
    item_id = item_controller.create_item(name="Test Item")
    
    # Add metadata
    db.items.add_metadata(item_id, "color", "red")
    db.items.add_metadata(item_id, "size", "large")
    
    # Retrieve metadata
    metadata = db.items.get_metadata(item_id)
    assert len(metadata) == 2
    
    metadata_dict = {meta['key']: meta['value'] for meta in metadata}
    assert metadata_dict['color'] == "red"
    assert metadata_dict['size'] == "large"


def test_get_metadata_by_key(temp_db):
    """Test getting specific metadata by key."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create item and add metadata
    item_id = item_controller.create_item(name="Test Item")
    db.items.add_metadata(item_id, "color", "red")
    db.items.add_metadata(item_id, "size", "large")
    
    # Get specific metadata
    metadata = db.items.get_metadata(item_id, key="color")
    assert len(metadata) == 1
    assert metadata[0]['key'] == "color"
    assert metadata[0]['value'] == "red"


def test_update_metadata(temp_db):
    """Test updating existing metadata."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create item and add metadata
    item_id = item_controller.create_item(name="Test Item")
    db.items.add_metadata(item_id, "color", "red")
    
    # Update metadata
    db.items.update_metadata(item_id, "color", "blue")
    
    # Verify update
    metadata = db.items.get_metadata(item_id, key="color")
    assert len(metadata) == 1
    assert metadata[0]['value'] == "blue"


def test_delete_metadata_by_key(temp_db):
    """Test deleting specific metadata by key."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create item and add metadata
    item_id = item_controller.create_item(name="Test Item")
    db.items.add_metadata(item_id, "color", "red")
    db.items.add_metadata(item_id, "size", "large")
    
    # Delete specific metadata
    db.items.delete_metadata(item_id, key="color")
    
    # Verify deletion
    metadata = db.items.get_metadata(item_id)
    assert len(metadata) == 1
    assert metadata[0]['key'] == "size"


def test_delete_all_metadata(temp_db):
    """Test deleting all metadata for an item."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create item and add metadata
    item_id = item_controller.create_item(name="Test Item")
    db.items.add_metadata(item_id, "color", "red")
    db.items.add_metadata(item_id, "size", "large")
    db.items.add_metadata(item_id, "weight", "heavy")
    
    # Delete all metadata
    db.items.delete_metadata(item_id)
    
    # Verify all deleted
    metadata = db.items.get_metadata(item_id)
    assert len(metadata) == 0


def test_metadata_cascade_on_item_deletion(temp_db):
    """Test that metadata is deleted when item is deleted."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create item and add metadata
    item_id = item_controller.create_item(name="Test Item")
    db.items.add_metadata(item_id, "color", "red")
    db.items.add_metadata(item_id, "size", "large")
    
    # Delete item
    item_controller.delete_item(item_id)
    
    # Verify metadata is deleted (cascade)
    metadata = db.items.get_metadata(item_id)
    assert len(metadata) == 0


def test_metadata_unique_key_per_item(temp_db):
    """Test that each item can have unique keys."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create two items
    item1_id = item_controller.create_item(name="Item 1")
    item2_id = item_controller.create_item(name="Item 2")
    
    # Add same key to both items with different values
    db.items.add_metadata(item1_id, "color", "red")
    db.items.add_metadata(item2_id, "color", "blue")
    
    # Verify both have their own metadata
    metadata1 = db.items.get_metadata(item1_id, key="color")
    metadata2 = db.items.get_metadata(item2_id, key="color")
    
    assert len(metadata1) == 1
    assert len(metadata2) == 1
    assert metadata1[0]['value'] == "red"
    assert metadata2[0]['value'] == "blue"


def test_metadata_overwrite_existing_key(temp_db):
    """Test that adding metadata with existing key overwrites."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create item
    item_id = item_controller.create_item(name="Test Item")
    
    # Add metadata
    db.items.add_metadata(item_id, "color", "red")
    
    # Add same key with different value (should overwrite)
    db.items.add_metadata(item_id, "color", "blue")
    
    # Verify only one entry exists with new value
    metadata = db.items.get_metadata(item_id)
    assert len(metadata) == 1
    assert metadata[0]['value'] == "blue"


def test_metadata_empty_value(temp_db):
    """Test that metadata can have empty value."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create item
    item_id = item_controller.create_item(name="Test Item")
    
    # Add metadata with empty value
    db.items.add_metadata(item_id, "notes", "")
    
    # Verify metadata exists
    metadata = db.items.get_metadata(item_id, key="notes")
    assert len(metadata) == 1
    assert metadata[0]['value'] == ""

