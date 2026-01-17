"""Controller for report-related operations."""
from database.database import CraftCompassDB
from typing import Dict, Any, List


class ReportController:
    def __init__(self, db: CraftCompassDB):
        """
        Initialize the report controller.
        
        Args:
            db: CraftCompassDB instance
        """
        self.db = db

    def get_inventory_summary(self) -> Dict[str, Any]:
        """
        Get a summary of inventory statistics.
        
        Returns:
            Dictionary with inventory statistics
        """
        items = self.db.items.get_all_items()
        suppliers = self.db.suppliers.get_all_suppliers()
        projects = self.db.projects.get_all_projects()
        
        total_items = len(items)
        total_suppliers = len(suppliers)
        total_projects = len(projects)
        
        categories = {}
        for item in items:
            cat = item.get('category') or 'Uncategorized'
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            'total_items': total_items,
            'total_suppliers': total_suppliers,
            'total_projects': total_projects,
            'categories': categories
        }

