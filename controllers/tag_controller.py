"""Controller for tag-related operations."""
from database.database import CraftCompassDB
from models.tag import Tag
from typing import List, Optional, Dict, Any


class TagController:
    def __init__(self, db: CraftCompassDB):
        """
        Initialize the tag controller.
        
        Args:
            db: CraftCompassDB instance
        """
        self.db = db

    def create_tag(self, name: str, color: Optional[str] = None) -> int:
        """
        Create a new tag.
        
        Args:
            name: Tag name (required)
            color: Optional color code/name
        
        Returns:
            ID of the created tag
        """
        return self.db.tags.add_tag(name=name, color=color)

    def get_tag(self, tag_id: int) -> Optional[Tag]:
        """
        Get a tag by ID.
        
        Args:
            tag_id: Tag ID
        
        Returns:
            Tag object or None if not found
        """
        data = self.db.tags.get_tag_by_id(tag_id)
        if data:
            return Tag.from_dict(data)
        return None

    def get_all_tags(self) -> List[Tag]:
        """
        Get all tags.
        
        Returns:
            List of Tag objects
        """
        tags_data = self.db.tags.get_all_tags()
        return [Tag.from_dict(tag) for tag in tags_data]

    def update_tag(self, tag_id: int, name: Optional[str] = None, color: Optional[str] = None):
        """
        Update a tag.
        
        Args:
            tag_id: ID of tag to update
            name: New name
            color: New color
        """
        self.db.tags.update_tag(tag_id=tag_id, name=name, color=color)

    def delete_tag(self, tag_id: int):
        """
        Delete a tag.
        
        Args:
            tag_id: ID of tag to delete
        """
        self.db.tags.delete_tag(tag_id)

    def add_tag_to_item(self, item_id: int, tag_id: int):
        """
        Add a tag to an item.
        
        Args:
            item_id: Item ID
            tag_id: Tag ID
        """
        self.db.tags.add_tag_to_item(item_id, tag_id)

    def remove_tag_from_item(self, item_id: int, tag_id: int):
        """
        Remove a tag from an item.
        
        Args:
            item_id: Item ID
            tag_id: Tag ID
        """
        self.db.tags.remove_tag_from_item(item_id, tag_id)

    def get_item_tags(self, item_id: int) -> List[Tag]:
        """
        Get all tags for an item.
        
        Args:
            item_id: Item ID
        
        Returns:
            List of Tag objects
        """
        tags_data = self.db.tags.get_item_tags(item_id)
        return [Tag.from_dict(tag) for tag in tags_data]

    def add_tag_to_project(self, project_id: int, tag_id: int):
        """
        Add a tag to a project.
        
        Args:
            project_id: Project ID
            tag_id: Tag ID
        """
        self.db.tags.add_tag_to_project(project_id, tag_id)

    def remove_tag_from_project(self, project_id: int, tag_id: int):
        """
        Remove a tag from a project.
        
        Args:
            project_id: Project ID
            tag_id: Tag ID
        """
        self.db.tags.remove_tag_from_project(project_id, tag_id)

    def get_project_tags(self, project_id: int) -> List[Tag]:
        """
        Get all tags for a project.
        
        Args:
            project_id: Project ID
        
        Returns:
            List of Tag objects
        """
        tags_data = self.db.tags.get_project_tags(project_id)
        return [Tag.from_dict(tag) for tag in tags_data]

    def get_items_by_tag(self, tag_id: int) -> List[Dict[str, Any]]:
        """
        Get all items with a specific tag.
        
        Args:
            tag_id: Tag ID
        
        Returns:
            List of item dictionaries
        """
        return self.db.tags.get_items_by_tag(tag_id)

    def get_projects_by_tag(self, tag_id: int) -> List[Dict[str, Any]]:
        """
        Get all projects with a specific tag.
        
        Args:
            tag_id: Tag ID
        
        Returns:
            List of project dictionaries
        """
        return self.db.tags.get_projects_by_tag(tag_id)

