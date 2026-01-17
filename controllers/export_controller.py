"""Controller for export/import operations."""
from database.database import CraftCompassDB
from utils.export_service import (
    export_items_to_csv,
    export_projects_to_csv,
    export_suppliers_to_csv,
    export_all_to_json,
    create_backup
)
from utils.import_service import import_items_from_csv, import_from_json
from typing import Tuple, List


class ExportController:
    def __init__(self, db: CraftCompassDB):
        """
        Initialize the export controller.
        
        Args:
            db: CraftCompassDB instance
        """
        self.db = db

    def export_items_csv(self, file_path: str):
        """
        Export items to CSV file.
        
        Args:
            file_path: Path to save CSV file
        """
        export_items_to_csv(self.db, file_path)

    def export_projects_csv(self, file_path: str):
        """
        Export projects to CSV file.
        
        Args:
            file_path: Path to save CSV file
        """
        export_projects_to_csv(self.db, file_path)

    def export_suppliers_csv(self, file_path: str):
        """
        Export suppliers to CSV file.
        
        Args:
            file_path: Path to save CSV file
        """
        export_suppliers_to_csv(self.db, file_path)

    def export_all_json(self, file_path: str):
        """
        Export all data to JSON file.
        
        Args:
            file_path: Path to save JSON file
        """
        export_all_to_json(self.db, file_path)

    def create_backup(self, backup_dir: str) -> str:
        """
        Create a full database backup.
        
        Args:
            backup_dir: Directory to save backup
        
        Returns:
            Path to the backup file
        """
        return create_backup(self.db, backup_dir)

    def import_items_csv(self, file_path: str, conflict_resolution: str = 'skip') -> Tuple[int, int, List[str]]:
        """
        Import items from CSV file.
        
        Args:
            file_path: Path to CSV file
            conflict_resolution: How to handle conflicts ('skip', 'update', 'rename')
        
        Returns:
            Tuple of (imported_count, skipped_count, errors)
        """
        return import_items_from_csv(self.db, file_path, conflict_resolution)

    def import_from_json(self, file_path: str, conflict_resolution: str = 'skip') -> Tuple[int, int, List[str]]:
        """
        Import data from JSON backup file.
        
        Args:
            file_path: Path to JSON file
            conflict_resolution: How to handle conflicts ('skip', 'update', 'rename')
        
        Returns:
            Tuple of (imported_count, skipped_count, errors)
        """
        return import_from_json(self.db, file_path, conflict_resolution)

