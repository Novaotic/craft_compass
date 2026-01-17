"""Controller for item-related operations."""
from database.database import CraftCompassDB
from models.item import Item
from typing import List, Optional, Dict, Any


class ItemController:
    def __init__(self, db: CraftCompassDB):
        """
        Initialize the item controller.
        
        Args:
            db: CraftCompassDB instance
        """
        self.db = db

    def create_item(self, name: str, category: Optional[str] = None, 
                    quantity: Optional[float] = None, unit: Optional[str] = None,
                    supplier_id: Optional[int] = None, purchase_date: Optional[str] = None,
                    photo_path: Optional[str] = None) -> int:
        """
        Create a new item.
        
        Args:
            name: Item name (required)
            category: Item category
            quantity: Quantity value
            unit: Unit of measurement
            supplier_id: ID of the supplier
            purchase_date: Purchase date (YYYY-MM-DD format)
            photo_path: Path to item photo
        
        Returns:
            ID of the created item
        """
        return self.db.items.add_item(
            name=name,
            category=category,
            quantity=quantity,
            unit=unit,
            supplier_id=supplier_id,
            purchase_date=purchase_date,
            photo_path=photo_path
        )

    def get_item(self, item_id: int) -> Optional[Item]:
        """
        Get an item by ID.
        
        Args:
            item_id: Item ID
        
        Returns:
            Item object or None if not found
        """
        data = self.db.items.get_item_by_id(item_id)
        if data:
            return Item.from_dict(data)
        return None

    def get_all_items(self) -> List[Item]:
        """
        Get all items.
        
        Returns:
            List of Item objects
        """
        items_data = self.db.items.get_all_items()
        return [Item.from_dict(item) for item in items_data]

    def update_item(self, item_id: int, name: Optional[str] = None,
                    category: Optional[str] = None, quantity: Optional[float] = None,
                    unit: Optional[str] = None, supplier_id: Optional[int] = None,
                    purchase_date: Optional[str] = None, photo_path: Optional[str] = None):
        """
        Update an item.
        
        Args:
            item_id: ID of item to update
            name: New name
            category: New category
            quantity: New quantity
            unit: New unit
            supplier_id: New supplier ID
            purchase_date: New purchase date
            photo_path: New photo path
        """
        self.db.items.update_item(
            item_id=item_id,
            name=name,
            category=category,
            quantity=quantity,
            unit=unit,
            supplier_id=supplier_id,
            purchase_date=purchase_date,
            photo_path=photo_path
        )

    def delete_item(self, item_id: int):
        """
        Delete an item.
        
        Args:
            item_id: ID of item to delete
        """
        self.db.items.delete_item(item_id)
    
    def search_items(self, search_term: str) -> List[Item]:
        """
        Search items by name, category, or supplier name.
        
        Args:
            search_term: Search term to match against
        
        Returns:
            List of Item objects matching the search
        """
        items_data = self.db.items.search_items(search_term)
        return [Item.from_dict(item) for item in items_data]
    
    def filter_items(self, category: Optional[str] = None, supplier_id: Optional[int] = None,
                     date_from: Optional[str] = None, date_to: Optional[str] = None,
                     quantity_min: Optional[float] = None, quantity_max: Optional[float] = None) -> List[Item]:
        """
        Filter items by various criteria.
        
        Args:
            category: Filter by category
            supplier_id: Filter by supplier ID
            date_from: Filter by purchase date from (YYYY-MM-DD)
            date_to: Filter by purchase date to (YYYY-MM-DD)
            quantity_min: Minimum quantity
            quantity_max: Maximum quantity
        
        Returns:
            List of Item objects matching the filters
        """
        items_data = self.db.items.filter_items(
            category=category,
            supplier_id=supplier_id,
            date_from=date_from,
            date_to=date_to,
            quantity_min=quantity_min,
            quantity_max=quantity_max
        )
        return [Item.from_dict(item) for item in items_data]

