"""Tests for model classes."""
import pytest
from models.item import Item
from models.project import Project
from models.supplier import Supplier


class TestItem:
    """Tests for Item model."""
    
    def test_item_creation(self):
        """Test creating an item."""
        item = Item(
            name='Test Item',
            category='Electronics',
            quantity=10.0,
            unit='pieces',
            supplier_id=1,
            purchase_date='2024-01-15'
        )
        assert item.name == 'Test Item'
        assert item.category == 'Electronics'
        assert item.quantity == 10.0
        assert item.unit == 'pieces'
    
    def test_item_to_dict(self):
        """Test converting item to dictionary."""
        item = Item(
            name='Test Item',
            category='Electronics',
            quantity=10.0
        )
        item_dict = item.to_dict()
        
        assert isinstance(item_dict, dict)
        assert item_dict['name'] == 'Test Item'
        assert item_dict['category'] == 'Electronics'
        assert item_dict['quantity'] == 10.0
    
    def test_item_from_dict(self):
        """Test creating item from dictionary."""
        data = {
            'id': 1,
            'name': 'Test Item',
            'category': 'Electronics',
            'quantity': 10.0,
            'unit': 'pieces',
            'supplier_id': 1,
            'purchase_date': '2024-01-15',
            'photo_path': None
        }
        item = Item.from_dict(data)
        
        assert item.id == 1
        assert item.name == 'Test Item'
        assert item.category == 'Electronics'
        assert item.quantity == 10.0


class TestProject:
    """Tests for Project model."""
    
    def test_project_creation(self):
        """Test creating a project."""
        project = Project(
            name='Test Project',
            description='A test project',
            date_created='2024-01-20'
        )
        assert project.name == 'Test Project'
        assert project.description == 'A test project'
        assert project.date_created == '2024-01-20'
        assert project.materials_used == []
    
    def test_add_material(self):
        """Test adding materials to a project."""
        project = Project(name='Test Project')
        project.add_material(item_id=1, quantity_used=5.0)
        
        assert len(project.materials_used) == 1
        assert project.materials_used[0] == (1, 5.0)
    
    def test_project_to_dict(self):
        """Test converting project to dictionary."""
        project = Project(
            name='Test Project',
            description='A test project',
            date_created='2024-01-20'
        )
        project.add_material(1, 5.0)
        project_dict = project.to_dict()
        
        assert isinstance(project_dict, dict)
        assert project_dict['name'] == 'Test Project'
        assert project_dict['materials_used'] == [(1, 5.0)]
    
    def test_project_from_dict(self):
        """Test creating project from dictionary."""
        data = {
            'id': 1,
            'name': 'Test Project',
            'description': 'A test project',
            'date_created': '2024-01-20'
        }
        project = Project.from_dict(data)
        
        assert project.id == 1
        assert project.name == 'Test Project'
        assert project.description == 'A test project'


class TestSupplier:
    """Tests for Supplier model."""
    
    def test_supplier_creation(self):
        """Test creating a supplier."""
        supplier = Supplier(
            name='Test Supplier',
            contact_info='test@example.com',
            website='https://example.com',
            notes='Test notes'
        )
        assert supplier.name == 'Test Supplier'
        assert supplier.contact_info == 'test@example.com'
        assert supplier.website == 'https://example.com'
    
    def test_supplier_to_dict(self):
        """Test converting supplier to dictionary."""
        supplier = Supplier(
            name='Test Supplier',
            contact_info='test@example.com'
        )
        supplier_dict = supplier.to_dict()
        
        assert isinstance(supplier_dict, dict)
        assert supplier_dict['name'] == 'Test Supplier'
        assert supplier_dict['contact_info'] == 'test@example.com'

