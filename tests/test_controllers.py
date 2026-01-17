"""Tests for controller classes."""
import pytest
from controllers.item_controllers import ItemController
from controllers.project_controller import ProjectController
from controllers.report_controller import ReportController


class TestItemController:
    """Tests for ItemController."""
    
    def test_create_item(self, temp_db):
        """Test creating an item via controller."""
        controller = ItemController(temp_db)
        item_id = controller.create_item(
            name='Test Item',
            category='Electronics',
            quantity=10.0,
            unit='pieces'
        )
        assert item_id is not None
        assert item_id > 0
    
    def test_get_item(self, temp_db):
        """Test retrieving an item via controller."""
        controller = ItemController(temp_db)
        item_id = controller.create_item(name='Test Item', category='Electronics')
        
        item = controller.get_item(item_id)
        assert item is not None
        assert item.name == 'Test Item'
        assert item.category == 'Electronics'
    
    def test_get_all_items(self, temp_db):
        """Test retrieving all items via controller."""
        controller = ItemController(temp_db)
        controller.create_item(name='Item 1')
        controller.create_item(name='Item 2')
        
        items = controller.get_all_items()
        assert len(items) >= 2
    
    def test_update_item(self, temp_db):
        """Test updating an item via controller."""
        controller = ItemController(temp_db)
        item_id = controller.create_item(name='Test Item')
        controller.update_item(item_id, name='Updated Item')
        
        item = controller.get_item(item_id)
        assert item.name == 'Updated Item'
    
    def test_delete_item(self, temp_db):
        """Test deleting an item via controller."""
        controller = ItemController(temp_db)
        item_id = controller.create_item(name='Test Item')
        controller.delete_item(item_id)
        
        item = controller.get_item(item_id)
        assert item is None


class TestProjectController:
    """Tests for ProjectController."""
    
    def test_create_project(self, temp_db):
        """Test creating a project via controller."""
        controller = ProjectController(temp_db)
        project_id = controller.create_project(
            name='Test Project',
            description='A test project'
        )
        assert project_id is not None
        assert project_id > 0
    
    def test_get_project(self, temp_db):
        """Test retrieving a project via controller."""
        controller = ProjectController(temp_db)
        project_id = controller.create_project(name='Test Project')
        
        project = controller.get_project(project_id)
        assert project is not None
        assert project.name == 'Test Project'
    
    def test_add_material_to_project(self, temp_db):
        """Test adding materials to a project."""
        controller = ProjectController(temp_db)
        item_controller = ItemController(temp_db)
        
        # Create item and project
        item_id = item_controller.create_item(name='Test Item')
        project_id = controller.create_project(name='Test Project')
        
        # Add material
        material_id = controller.add_material_to_project(project_id, item_id, 5.0)
        assert material_id is not None
        
        # Verify material was added
        materials = controller.get_project_materials(project_id)
        assert len(materials) == 1
        assert materials[0]['quantity_used'] == 5.0
    
    def test_delete_project(self, temp_db):
        """Test deleting a project via controller."""
        controller = ProjectController(temp_db)
        project_id = controller.create_project(name='Test Project')
        controller.delete_project(project_id)
        
        project = controller.get_project(project_id)
        assert project is None


class TestReportController:
    """Tests for ReportController."""
    
    def test_get_inventory_summary(self, temp_db):
        """Test getting inventory summary."""
        controller = ReportController(temp_db)
        
        # Add some test data
        temp_db.items.add_item(name='Item 1', category='Electronics')
        temp_db.items.add_item(name='Item 2', category='Electronics')
        temp_db.items.add_item(name='Item 3', category='Tools')
        temp_db.suppliers.add_supplier('Supplier 1', 'contact@example.com')
        temp_db.projects.add_project(name='Project 1')
        
        summary = controller.get_inventory_summary()
        
        assert summary['total_items'] == 3
        assert summary['total_suppliers'] == 1
        assert summary['total_projects'] == 1
        assert 'Electronics' in summary['categories']
        assert summary['categories']['Electronics'] == 2
        assert summary['categories']['Tools'] == 1

