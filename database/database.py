from database.db_manager import (
    DatabaseAdmin,
    SupplierManager,
    ItemManager,
    ProjectManager,
    ProjectMaterialManager,
    TagManager
)

class CraftCompassDB:
    def __init__(self, db_path=None):
        """
        Initialize Craft Compass database connection.
        
        Args:
            db_path: Optional path to SQLite database file. 
                    If None, uses default 'craft_compass.db' in project root.
        """
        self.admin = DatabaseAdmin(db_path)
        self.suppliers = SupplierManager(db_path)
        self.items = ItemManager(db_path)
        self.projects = ProjectManager(db_path)
        self.materials = ProjectMaterialManager(db_path)
        self.tags = TagManager(db_path)

    def initialize(self):
        """Initialize the database with the schema."""
        self.admin.initialize_database()
