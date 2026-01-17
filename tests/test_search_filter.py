"""Tests for search and filter functionality."""
import pytest
from database.database import CraftCompassDB
from controllers.item_controllers import ItemController
from controllers.project_controller import ProjectController


def test_search_items_by_name(temp_db):
    """Test searching items by name."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create test items
    item_controller.create_item(name="Red Yarn", category="Yarn", quantity=5.0, unit="skein")
    item_controller.create_item(name="Blue Thread", category="Thread", quantity=10.0, unit="spool")
    item_controller.create_item(name="Green Fabric", category="Fabric", quantity=2.0, unit="yard")
    
    # Search for "Red"
    results = item_controller.search_items("Red")
    assert len(results) == 1
    assert results[0].name == "Red Yarn"
    
    # Search for "Thread"
    results = item_controller.search_items("Thread")
    assert len(results) == 1
    assert results[0].name == "Blue Thread"


def test_search_items_by_category(temp_db):
    """Test searching items by category."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create test items
    item_controller.create_item(name="Red Yarn", category="Yarn", quantity=5.0)
    item_controller.create_item(name="Blue Yarn", category="Yarn", quantity=3.0)
    item_controller.create_item(name="Green Fabric", category="Fabric", quantity=2.0)
    
    # Search for "Yarn"
    results = item_controller.search_items("Yarn")
    assert len(results) == 2
    assert all(item.category == "Yarn" for item in results)


def test_filter_items_by_category(temp_db):
    """Test filtering items by category."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create test items
    item_controller.create_item(name="Red Yarn", category="Yarn", quantity=5.0)
    item_controller.create_item(name="Blue Thread", category="Thread", quantity=10.0)
    item_controller.create_item(name="Green Fabric", category="Fabric", quantity=2.0)
    
    # Filter by category
    results = item_controller.filter_items(category="Yarn")
    assert len(results) == 1
    assert results[0].category == "Yarn"


def test_filter_items_by_quantity_range(temp_db):
    """Test filtering items by quantity range."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create test items
    item_controller.create_item(name="Item 1", quantity=5.0)
    item_controller.create_item(name="Item 2", quantity=10.0)
    item_controller.create_item(name="Item 3", quantity=15.0)
    
    # Filter by quantity range
    results = item_controller.filter_items(quantity_min=8.0, quantity_max=12.0)
    assert len(results) == 1
    assert results[0].name == "Item 2"


def test_filter_items_by_date_range(temp_db):
    """Test filtering items by purchase date range."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create test items with dates
    item_controller.create_item(name="Item 1", purchase_date="2024-01-15")
    item_controller.create_item(name="Item 2", purchase_date="2024-02-15")
    item_controller.create_item(name="Item 3", purchase_date="2024-03-15")
    
    # Filter by date range
    results = item_controller.filter_items(date_from="2024-02-01", date_to="2024-02-28")
    assert len(results) == 1
    assert results[0].name == "Item 2"


def test_search_projects_by_name(temp_db):
    """Test searching projects by name."""
    db = temp_db
    project_controller = ProjectController(db)
    
    # Create test projects
    project_controller.create_project(name="Scarf Project", description="Making a scarf")
    project_controller.create_project(name="Hat Project", description="Making a hat")
    
    # Search for "Scarf"
    results = project_controller.search_projects("Scarf")
    assert len(results) == 1
    assert results[0].name == "Scarf Project"


def test_search_projects_by_description(temp_db):
    """Test searching projects by description."""
    db = temp_db
    project_controller = ProjectController(db)
    
    # Create test projects
    project_controller.create_project(name="Project 1", description="Making a scarf")
    project_controller.create_project(name="Project 2", description="Making a hat")
    
    # Search for "scarf"
    results = project_controller.search_projects("scarf")
    assert len(results) == 1
    assert results[0].description == "Making a scarf"


def test_filter_projects_by_date_range(temp_db):
    """Test filtering projects by date range."""
    db = temp_db
    project_controller = ProjectController(db)
    
    # Create test projects
    project_controller.create_project(name="Project 1", date_created="2024-01-15")
    project_controller.create_project(name="Project 2", date_created="2024-02-15")
    project_controller.create_project(name="Project 3", date_created="2024-03-15")
    
    # Filter by date range
    results = project_controller.filter_projects(date_from="2024-02-01", date_to="2024-02-28")
    assert len(results) == 1
    assert results[0].name == "Project 2"


def test_search_suppliers(temp_db):
    """Test searching suppliers."""
    db = temp_db
    
    # Create test suppliers
    db.suppliers.add_supplier(name="Yarn Store", contact_info="123 Main St")
    db.suppliers.add_supplier(name="Fabric Shop", contact_info="456 Oak Ave")
    
    # Search for "Yarn"
    results = db.suppliers.search_suppliers("Yarn")
    assert len(results) == 1
    assert results[0]['name'] == "Yarn Store"
    
    # Search for "Oak"
    results = db.suppliers.search_suppliers("Oak")
    assert len(results) == 1
    assert results[0]['name'] == "Fabric Shop"


def test_empty_search_results(temp_db):
    """Test that empty search returns no results."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Search with no matching items
    results = item_controller.search_items("NonExistentItem")
    assert len(results) == 0


def test_combined_search_and_filter(temp_db):
    """Test combining search and filter (search first, then filter)."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create test items
    item_controller.create_item(name="Red Yarn", category="Yarn", quantity=5.0)
    item_controller.create_item(name="Blue Yarn", category="Yarn", quantity=3.0)
    item_controller.create_item(name="Red Fabric", category="Fabric", quantity=2.0)
    
    # Search for "Red", then manually filter by category
    search_results = item_controller.search_items("Red")
    filtered = [item for item in search_results if item.category == "Yarn"]
    assert len(filtered) == 1
    assert filtered[0].name == "Red Yarn"

