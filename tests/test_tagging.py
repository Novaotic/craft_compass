"""Tests for tagging system."""
import pytest
from database.database import CraftCompassDB
from controllers.tag_controller import TagController
from controllers.item_controllers import ItemController
from controllers.project_controller import ProjectController


def test_create_tag(temp_db):
    """Test creating a tag."""
    db = temp_db
    tag_controller = TagController(db)
    
    tag_id = tag_controller.create_tag(name="Test Tag", color="red")
    assert tag_id is not None
    
    tag = tag_controller.get_tag(tag_id)
    assert tag is not None
    assert tag.name == "Test Tag"
    assert tag.color == "red"


def test_get_all_tags(temp_db):
    """Test getting all tags."""
    db = temp_db
    tag_controller = TagController(db)
    
    tag_controller.create_tag(name="Tag 1")
    tag_controller.create_tag(name="Tag 2")
    tag_controller.create_tag(name="Tag 3")
    
    tags = tag_controller.get_all_tags()
    assert len(tags) == 3
    tag_names = [tag.name for tag in tags]
    assert "Tag 1" in tag_names
    assert "Tag 2" in tag_names
    assert "Tag 3" in tag_names


def test_update_tag(temp_db):
    """Test updating a tag."""
    db = temp_db
    tag_controller = TagController(db)
    
    tag_id = tag_controller.create_tag(name="Old Name", color="red")
    tag_controller.update_tag(tag_id, name="New Name", color="blue")
    
    tag = tag_controller.get_tag(tag_id)
    assert tag.name == "New Name"
    assert tag.color == "blue"


def test_delete_tag(temp_db):
    """Test deleting a tag."""
    db = temp_db
    tag_controller = TagController(db)
    
    tag_id = tag_controller.create_tag(name="To Delete")
    tag_controller.delete_tag(tag_id)
    
    tag = tag_controller.get_tag(tag_id)
    assert tag is None


def test_add_tag_to_item(temp_db):
    """Test adding a tag to an item."""
    db = temp_db
    tag_controller = TagController(db)
    item_controller = ItemController(db)
    
    # Create item and tag
    item_id = item_controller.create_item(name="Test Item")
    tag_id = tag_controller.create_tag(name="Test Tag")
    
    # Add tag to item
    tag_controller.add_tag_to_item(item_id, tag_id)
    
    # Verify tag is associated
    item_tags = tag_controller.get_item_tags(item_id)
    assert len(item_tags) == 1
    assert item_tags[0].id == tag_id


def test_remove_tag_from_item(temp_db):
    """Test removing a tag from an item."""
    db = temp_db
    tag_controller = TagController(db)
    item_controller = ItemController(db)
    
    # Create item and tag
    item_id = item_controller.create_item(name="Test Item")
    tag_id = tag_controller.create_tag(name="Test Tag")
    
    # Add and then remove tag
    tag_controller.add_tag_to_item(item_id, tag_id)
    tag_controller.remove_tag_from_item(item_id, tag_id)
    
    # Verify tag is removed
    item_tags = tag_controller.get_item_tags(item_id)
    assert len(item_tags) == 0


def test_add_tag_to_project(temp_db):
    """Test adding a tag to a project."""
    db = temp_db
    tag_controller = TagController(db)
    project_controller = ProjectController(db)
    
    # Create project and tag
    project_id = project_controller.create_project(name="Test Project")
    tag_id = tag_controller.create_tag(name="Test Tag")
    
    # Add tag to project
    tag_controller.add_tag_to_project(project_id, tag_id)
    
    # Verify tag is associated
    project_tags = tag_controller.get_project_tags(project_id)
    assert len(project_tags) == 1
    assert project_tags[0].id == tag_id


def test_remove_tag_from_project(temp_db):
    """Test removing a tag from a project."""
    db = temp_db
    tag_controller = TagController(db)
    project_controller = ProjectController(db)
    
    # Create project and tag
    project_id = project_controller.create_project(name="Test Project")
    tag_id = tag_controller.create_tag(name="Test Tag")
    
    # Add and then remove tag
    tag_controller.add_tag_to_project(project_id, tag_id)
    tag_controller.remove_tag_from_project(project_id, tag_id)
    
    # Verify tag is removed
    project_tags = tag_controller.get_project_tags(project_id)
    assert len(project_tags) == 0


def test_get_items_by_tag(temp_db):
    """Test getting all items with a specific tag."""
    db = temp_db
    tag_controller = TagController(db)
    item_controller = ItemController(db)
    
    # Create items and tag
    item1_id = item_controller.create_item(name="Item 1")
    item2_id = item_controller.create_item(name="Item 2")
    item3_id = item_controller.create_item(name="Item 3")
    tag_id = tag_controller.create_tag(name="Common Tag")
    
    # Add tag to items 1 and 2
    tag_controller.add_tag_to_item(item1_id, tag_id)
    tag_controller.add_tag_to_item(item2_id, tag_id)
    
    # Get items by tag
    items = tag_controller.get_items_by_tag(tag_id)
    assert len(items) == 2
    item_ids = [item['id'] for item in items]
    assert item1_id in item_ids
    assert item2_id in item_ids
    assert item3_id not in item_ids


def test_get_projects_by_tag(temp_db):
    """Test getting all projects with a specific tag."""
    db = temp_db
    tag_controller = TagController(db)
    project_controller = ProjectController(db)
    
    # Create projects and tag
    project1_id = project_controller.create_project(name="Project 1")
    project2_id = project_controller.create_project(name="Project 2")
    project3_id = project_controller.create_project(name="Project 3")
    tag_id = tag_controller.create_tag(name="Common Tag")
    
    # Add tag to projects 1 and 2
    tag_controller.add_tag_to_project(project1_id, tag_id)
    tag_controller.add_tag_to_project(project2_id, tag_id)
    
    # Get projects by tag
    projects = tag_controller.get_projects_by_tag(tag_id)
    assert len(projects) == 2
    project_ids = [project['id'] for project in projects]
    assert project1_id in project_ids
    assert project2_id in project_ids
    assert project3_id not in project_ids


def test_tag_deletion_cascade(temp_db):
    """Test that tag deletion cascades to associations."""
    db = temp_db
    tag_controller = TagController(db)
    item_controller = ItemController(db)
    
    # Create item and tag
    item_id = item_controller.create_item(name="Test Item")
    tag_id = tag_controller.create_tag(name="Test Tag")
    
    # Add tag to item
    tag_controller.add_tag_to_item(item_id, tag_id)
    
    # Delete tag
    tag_controller.delete_tag(tag_id)
    
    # Verify tag is deleted and association is removed
    tag = tag_controller.get_tag(tag_id)
    assert tag is None
    
    item_tags = tag_controller.get_item_tags(item_id)
    assert len(item_tags) == 0


def test_multiple_tags_on_item(temp_db):
    """Test adding multiple tags to an item."""
    db = temp_db
    tag_controller = TagController(db)
    item_controller = ItemController(db)
    
    # Create item and multiple tags
    item_id = item_controller.create_item(name="Test Item")
    tag1_id = tag_controller.create_tag(name="Tag 1")
    tag2_id = tag_controller.create_tag(name="Tag 2")
    tag3_id = tag_controller.create_tag(name="Tag 3")
    
    # Add multiple tags
    tag_controller.add_tag_to_item(item_id, tag1_id)
    tag_controller.add_tag_to_item(item_id, tag2_id)
    tag_controller.add_tag_to_item(item_id, tag3_id)
    
    # Verify all tags are associated
    item_tags = tag_controller.get_item_tags(item_id)
    assert len(item_tags) == 3
    tag_ids = [tag.id for tag in item_tags]
    assert tag1_id in tag_ids
    assert tag2_id in tag_ids
    assert tag3_id in tag_ids

