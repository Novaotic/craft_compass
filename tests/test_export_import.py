"""Tests for export and import functionality."""
import pytest
import os
import json
import csv
import tempfile
from database.database import CraftCompassDB
from controllers.item_controllers import ItemController
from controllers.project_controller import ProjectController
from controllers.tag_controller import TagController
from utils.export_service import export_items_to_csv, export_projects_to_csv, export_suppliers_to_csv, export_all_to_json
from utils.import_service import import_items_from_csv, import_from_json


def test_export_items_to_csv(temp_db):
    """Test exporting items to CSV."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create test items
    item_controller.create_item(name="Item 1", category="Category A", quantity=5.0, unit="pcs")
    item_controller.create_item(name="Item 2", category="Category B", quantity=10.0, unit="pcs")
    
    # Export to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        csv_path = f.name
    
    try:
        export_items_to_csv(db, csv_path)
        
        # Verify file exists and has content
        assert os.path.exists(csv_path)
        
        # Read and verify CSV content
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 2
            assert rows[0]['name'] == "Item 1"
            assert rows[1]['name'] == "Item 2"
    finally:
        if os.path.exists(csv_path):
            os.remove(csv_path)


def test_export_projects_to_csv(temp_db):
    """Test exporting projects to CSV."""
    db = temp_db
    project_controller = ProjectController(db)
    
    # Create test projects
    project_controller.create_project(name="Project 1", description="Description 1")
    project_controller.create_project(name="Project 2", description="Description 2")
    
    # Export to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        csv_path = f.name
    
    try:
        export_projects_to_csv(db, csv_path)
        
        # Verify file exists
        assert os.path.exists(csv_path)
        
        # Read and verify CSV content
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 2
            assert rows[0]['name'] == "Project 1"
            assert rows[1]['name'] == "Project 2"
    finally:
        if os.path.exists(csv_path):
            os.remove(csv_path)


def test_export_suppliers_to_csv(temp_db):
    """Test exporting suppliers to CSV."""
    db = temp_db
    
    # Create test suppliers
    db.suppliers.add_supplier(name="Supplier 1", contact_info="Contact 1")
    db.suppliers.add_supplier(name="Supplier 2", contact_info="Contact 2")
    
    # Export to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        csv_path = f.name
    
    try:
        export_suppliers_to_csv(db, csv_path)
        
        # Verify file exists
        assert os.path.exists(csv_path)
        
        # Read and verify CSV content
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 2
            assert rows[0]['name'] == "Supplier 1"
            assert rows[1]['name'] == "Supplier 2"
    finally:
        if os.path.exists(csv_path):
            os.remove(csv_path)


def test_export_all_to_json(temp_db):
    """Test exporting all data to JSON."""
    db = temp_db
    item_controller = ItemController(db)
    project_controller = ProjectController(db)
    tag_controller = TagController(db)
    
    # Create test data
    supplier_id = db.suppliers.add_supplier(name="Test Supplier", contact_info="Contact")
    item_id = item_controller.create_item(name="Test Item", supplier_id=supplier_id)
    project_id = project_controller.create_project(name="Test Project")
    tag_id = tag_controller.create_tag(name="Test Tag")
    
    # Add associations
    tag_controller.add_tag_to_item(item_id, tag_id)
    tag_controller.add_tag_to_project(project_id, tag_id)
    db.items.add_metadata(item_id, "key1", "value1")
    
    # Export to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json_path = f.name
    
    try:
        export_all_to_json(db, json_path)
        
        # Verify file exists
        assert os.path.exists(json_path)
        
        # Read and verify JSON content
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert 'data' in data
            assert 'suppliers' in data['data']
            assert 'items' in data['data']
            assert 'projects' in data['data']
            assert 'tags' in data['data']
            assert 'item_tags' in data['data']
            assert 'project_tags' in data['data']
            assert 'item_metadata' in data['data']
    finally:
        if os.path.exists(json_path):
            os.remove(json_path)


def test_import_items_from_csv_skip(temp_db):
    """Test importing items from CSV with skip conflict resolution."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create existing item
    item_controller.create_item(name="Existing Item", category="Category A")
    
    # Create CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        csv_path = f.name
        writer = csv.DictWriter(f, fieldnames=['name', 'category', 'quantity', 'unit', 'supplier', 'purchase_date', 'photo_path'])
        writer.writeheader()
        writer.writerow({'name': 'Existing Item', 'category': 'Category B', 'quantity': '10', 'unit': 'pcs', 'supplier': '', 'purchase_date': '', 'photo_path': ''})
        writer.writerow({'name': 'New Item', 'category': 'Category C', 'quantity': '5', 'unit': 'pcs', 'supplier': '', 'purchase_date': '', 'photo_path': ''})
    
    try:
        imported, skipped, errors = import_items_from_csv(db, csv_path, conflict_resolution='skip')
        
        # Should import 1, skip 1
        assert imported == 1
        assert skipped == 1
        
        # Verify new item was imported
        items = item_controller.get_all_items()
        item_names = [item.name for item in items]
        assert "New Item" in item_names
        assert "Existing Item" in item_names
    finally:
        if os.path.exists(csv_path):
            os.remove(csv_path)


def test_import_items_from_csv_update(temp_db):
    """Test importing items from CSV with update conflict resolution."""
    db = temp_db
    item_controller = ItemController(db)
    
    # Create existing item
    item_controller.create_item(name="Existing Item", category="Category A", quantity=5.0)
    
    # Create CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        csv_path = f.name
        writer = csv.DictWriter(f, fieldnames=['name', 'category', 'quantity', 'unit', 'supplier', 'purchase_date', 'photo_path'])
        writer.writeheader()
        writer.writerow({'name': 'Existing Item', 'category': 'Category B', 'quantity': '10', 'unit': 'pcs', 'supplier': '', 'purchase_date': '', 'photo_path': ''})
    
    try:
        imported, skipped, errors = import_items_from_csv(db, csv_path, conflict_resolution='update')
        
        # Should update 1
        assert imported == 1
        
        # Verify item was updated
        items = item_controller.get_all_items()
        updated_item = next((item for item in items if item.name == "Existing Item"), None)
        assert updated_item is not None
        assert updated_item.category == "Category B"
    finally:
        if os.path.exists(csv_path):
            os.remove(csv_path)


def test_import_from_json(temp_db):
    """Test importing data from JSON backup."""
    db = temp_db
    item_controller = ItemController(db)
    project_controller = ProjectController(db)
    
    # Create some test data first
    supplier_id = db.suppliers.add_supplier(name="Test Supplier", contact_info="Contact")
    item_id = item_controller.create_item(name="Test Item", supplier_id=supplier_id)
    project_id = project_controller.create_project(name="Test Project")
    
    # Create JSON export file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json_path = f.name
    
    try:
        # First export current data
        export_all_to_json(db, json_path)
        
        # Clear database (simulate fresh import)
        items = db.items.get_all_items()
        for item in items:
            db.items.delete_item(item['id'])
        suppliers = db.suppliers.get_all_suppliers()
        for supplier in suppliers:
            db.suppliers.delete_supplier(supplier['id'])
        projects = db.projects.get_all_projects()
        for project in projects:
            db.projects.delete_project(project['id'])
        
        # Import from JSON
        imported, skipped, errors = import_from_json(db, json_path, conflict_resolution='skip')
        
        # Verify data was imported
        assert imported > 0
    finally:
        if os.path.exists(json_path):
            os.remove(json_path)


def test_export_empty_database(temp_db):
    """Test exporting empty database."""
    db = temp_db
    
    # Export to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        csv_path = f.name
    
    try:
        export_items_to_csv(db, csv_path)
        
        # File should exist (even if empty)
        assert os.path.exists(csv_path)
    finally:
        if os.path.exists(csv_path):
            os.remove(csv_path)


def test_import_invalid_csv(temp_db):
    """Test importing invalid CSV file."""
    db = temp_db
    
    # Create invalid CSV file (missing required 'name' field)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        csv_path = f.name
        writer = csv.DictWriter(f, fieldnames=['name', 'category', 'quantity', 'unit', 'supplier', 'purchase_date', 'photo_path'])
        writer.writeheader()
        writer.writerow({'name': '', 'category': 'Category', 'quantity': '10', 'unit': 'pcs', 'supplier': '', 'purchase_date': '', 'photo_path': ''})
    
    try:
        imported, skipped, errors = import_items_from_csv(db, csv_path, conflict_resolution='skip')
        
        # Should have errors (missing name field)
        assert len(errors) > 0
    finally:
        if os.path.exists(csv_path):
            os.remove(csv_path)

