"""Tests for database manager operations."""
import pytest
from database.db_manager import (
    SupplierManager,
    ItemManager,
    ProjectManager,
    ProjectMaterialManager
)


class TestSupplierManager:
    """Tests for SupplierManager."""
    
    def test_add_supplier(self, temp_db):
        """Test adding a supplier."""
        supplier_id = temp_db.suppliers.add_supplier(
            name='Test Supplier',
            contact_info='test@example.com',
            website='https://example.com',
            notes='Test notes'
        )
        assert supplier_id is not None
        assert supplier_id > 0
    
    def test_get_supplier_by_id(self, temp_db, sample_supplier):
        """Test retrieving a supplier by ID."""
        supplier_id = temp_db.suppliers.add_supplier(**sample_supplier)
        supplier = temp_db.suppliers.get_supplier_by_id(supplier_id)
        
        assert supplier is not None
        assert supplier['name'] == sample_supplier['name']
        assert supplier['contact_info'] == sample_supplier['contact_info']
    
    def test_get_all_suppliers(self, temp_db):
        """Test retrieving all suppliers."""
        # Add multiple suppliers
        temp_db.suppliers.add_supplier('Supplier 1', 'contact1@example.com')
        temp_db.suppliers.add_supplier('Supplier 2', 'contact2@example.com')
        
        suppliers = temp_db.suppliers.get_all_suppliers()
        assert len(suppliers) >= 2
    
    def test_update_supplier(self, temp_db, sample_supplier):
        """Test updating a supplier."""
        supplier_id = temp_db.suppliers.add_supplier(**sample_supplier)
        temp_db.suppliers.update_supplier(supplier_id, name='Updated Name')
        
        supplier = temp_db.suppliers.get_supplier_by_id(supplier_id)
        assert supplier['name'] == 'Updated Name'
    
    def test_delete_supplier(self, temp_db, sample_supplier):
        """Test deleting a supplier."""
        supplier_id = temp_db.suppliers.add_supplier(**sample_supplier)
        temp_db.suppliers.delete_supplier(supplier_id)
        
        supplier = temp_db.suppliers.get_supplier_by_id(supplier_id)
        assert supplier is None


class TestItemManager:
    """Tests for ItemManager."""
    
    def test_add_item(self, temp_db, sample_item):
        """Test adding an item."""
        item_id = temp_db.items.add_item(**sample_item)
        assert item_id is not None
        assert item_id > 0
    
    def test_get_item_by_id(self, temp_db, sample_item):
        """Test retrieving an item by ID."""
        item_id = temp_db.items.add_item(**sample_item)
        item = temp_db.items.get_item_by_id(item_id)
        
        assert item is not None
        assert item['name'] == sample_item['name']
        assert item['category'] == sample_item['category']
    
    def test_get_all_items(self, temp_db, sample_item):
        """Test retrieving all items."""
        temp_db.items.add_item(**sample_item)
        sample_item2 = sample_item.copy()
        sample_item2['name'] = 'Item 2'
        temp_db.items.add_item(**sample_item2)
        
        items = temp_db.items.get_all_items()
        assert len(items) >= 2
    
    def test_update_item(self, temp_db, sample_item):
        """Test updating an item."""
        item_id = temp_db.items.add_item(**sample_item)
        temp_db.items.update_item(item_id, name='Updated Item', quantity=20.0)
        
        item = temp_db.items.get_item_by_id(item_id)
        assert item['name'] == 'Updated Item'
        assert item['quantity'] == 20.0
    
    def test_delete_item(self, temp_db, sample_item):
        """Test deleting an item."""
        item_id = temp_db.items.add_item(**sample_item)
        temp_db.items.delete_item(item_id)
        
        item = temp_db.items.get_item_by_id(item_id)
        assert item is None


class TestProjectManager:
    """Tests for ProjectManager."""
    
    def test_add_project(self, temp_db, sample_project):
        """Test adding a project."""
        project_id = temp_db.projects.add_project(**sample_project)
        assert project_id is not None
        assert project_id > 0
    
    def test_get_project_by_id(self, temp_db, sample_project):
        """Test retrieving a project by ID."""
        project_id = temp_db.projects.add_project(**sample_project)
        project = temp_db.projects.get_project_by_id(project_id)
        
        assert project is not None
        assert project['name'] == sample_project['name']
    
    def test_get_all_projects(self, temp_db, sample_project):
        """Test retrieving all projects."""
        temp_db.projects.add_project(**sample_project)
        project2 = sample_project.copy()
        project2['name'] = 'Project 2'
        temp_db.projects.add_project(**project2)
        
        projects = temp_db.projects.get_all_projects()
        assert len(projects) >= 2
    
    def test_update_project(self, temp_db, sample_project):
        """Test updating a project."""
        project_id = temp_db.projects.add_project(**sample_project)
        temp_db.projects.update_project(project_id, name='Updated Project')
        
        project = temp_db.projects.get_project_by_id(project_id)
        assert project['name'] == 'Updated Project'
    
    def test_delete_project(self, temp_db, sample_project):
        """Test deleting a project."""
        project_id = temp_db.projects.add_project(**sample_project)
        temp_db.projects.delete_project(project_id)
        
        project = temp_db.projects.get_project_by_id(project_id)
        assert project is None


class TestProjectMaterialManager:
    """Tests for ProjectMaterialManager."""
    
    def test_add_project_material(self, temp_db, sample_item, sample_project):
        """Test adding a material to a project."""
        item_id = temp_db.items.add_item(**sample_item)
        project_id = temp_db.projects.add_project(**sample_project)
        
        material_id = temp_db.materials.add_project_material(project_id, item_id, 5.0)
        assert material_id is not None
        assert material_id > 0
    
    def test_get_materials_by_project(self, temp_db, sample_item, sample_project):
        """Test retrieving materials for a project."""
        item_id = temp_db.items.add_item(**sample_item)
        project_id = temp_db.projects.add_project(**sample_project)
        temp_db.materials.add_project_material(project_id, item_id, 5.0)
        
        materials = temp_db.materials.get_materials_by_project(project_id)
        assert len(materials) == 1
        assert materials[0]['quantity_used'] == 5.0
    
    def test_delete_project_material(self, temp_db, sample_item, sample_project):
        """Test deleting a project material."""
        item_id = temp_db.items.add_item(**sample_item)
        project_id = temp_db.projects.add_project(**sample_project)
        material_id = temp_db.materials.add_project_material(project_id, item_id, 5.0)
        
        temp_db.materials.delete_project_material(material_id)
        materials = temp_db.materials.get_materials_by_project(project_id)
        assert len(materials) == 0

