import sqlite3
import os
from typing import Optional, List, Dict, Any

DB_NAME = 'craft_compass.db'
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

class BaseManager:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            # Default to project root directory
            project_root = os.path.dirname(os.path.dirname(__file__))
            db_path = os.path.join(project_root, DB_NAME)
        self.db_path = db_path

    def get_connection(self):
        """Get a SQLite database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        return conn

    def execute_query(self, query: str, params: tuple = ()):
        """Execute a query that modifies data (INSERT, UPDATE, DELETE)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            # Return lastrowid for INSERT operations
            return cursor.lastrowid

    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Fetch all rows from a query and return as list of dictionaries."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            # Convert Row objects to dictionaries
            return [dict(row) for row in rows]

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """Fetch one row from a query and return as dictionary."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None


class DatabaseAdmin(BaseManager):
    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.schema_path = SCHEMA_PATH

    def initialize_database(self):
        """Initialize the database with the schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            with open(self.schema_path, 'r') as f:
                schema_sql = f.read()
                # Execute each statement separately
                for statement in schema_sql.split(';'):
                    statement = statement.strip()
                    if statement:
                        cursor.execute(statement)
            conn.commit()
        print(f"Database '{self.db_path}' initialized with schema from '{self.schema_path}'.")

    def reset_database(self):
        """Drop all tables and reinitialize the database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table['name']};")
            conn.commit()
        
        self.initialize_database()


class SupplierManager(BaseManager):
    def add_supplier(self, name: str, contact_info: str, website: Optional[str] = None, notes: Optional[str] = None) -> int:
        """Add a new supplier and return the supplier ID."""
        query = "INSERT INTO suppliers (name, contact_info, website, notes) VALUES (?, ?, ?, ?)"
        return self.execute_query(query, (name, contact_info, website, notes))

    def get_supplier_by_id(self, supplier_id: int) -> Optional[Dict[str, Any]]:
        """Get a supplier by ID."""
        return self.fetch_one("SELECT * FROM suppliers WHERE id = ?", (supplier_id,))

    def get_all_suppliers(self) -> List[Dict[str, Any]]:
        """Get all suppliers."""
        return self.fetch_all("SELECT * FROM suppliers ORDER BY name")

    def update_supplier(self, supplier_id: int, name: Optional[str] = None, contact_info: Optional[str] = None, 
                       website: Optional[str] = None, notes: Optional[str] = None):
        """Update a supplier. Only provided fields will be updated."""
        updates = []
        params = []
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if contact_info is not None:
            updates.append("contact_info = ?")
            params.append(contact_info)
        if website is not None:
            updates.append("website = ?")
            params.append(website)
        if notes is not None:
            updates.append("notes = ?")
            params.append(notes)
        
        if updates:
            params.append(supplier_id)
            query = f"UPDATE suppliers SET {', '.join(updates)} WHERE id = ?"
            self.execute_query(query, tuple(params))

    def delete_supplier(self, supplier_id: int):
        """Delete a supplier by ID."""
        self.execute_query("DELETE FROM suppliers WHERE id = ?", (supplier_id,))


class ItemManager(BaseManager):
    def add_item(self, name: str, category: Optional[str] = None, quantity: Optional[float] = None,
                 unit: Optional[str] = None, supplier_id: Optional[int] = None,
                 purchase_date: Optional[str] = None, photo_path: Optional[str] = None) -> int:
        """Add a new item and return the item ID."""
        query = """INSERT INTO items (name, category, quantity, unit, supplier_id, purchase_date, photo_path)
                   VALUES (?, ?, ?, ?, ?, ?, ?)"""
        return self.execute_query(query, (name, category, quantity, unit, supplier_id, purchase_date, photo_path))

    def get_item_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Get an item by ID."""
        return self.fetch_one("SELECT * FROM items WHERE id = ?", (item_id,))

    def get_all_items(self) -> List[Dict[str, Any]]:
        """Get all items."""
        return self.fetch_all("SELECT * FROM items ORDER BY name")

    def update_item(self, item_id: int, name: Optional[str] = None, category: Optional[str] = None,
                    quantity: Optional[float] = None, unit: Optional[str] = None,
                    supplier_id: Optional[int] = None, purchase_date: Optional[str] = None,
                    photo_path: Optional[str] = None):
        """Update an item. Only provided fields will be updated."""
        updates = []
        params = []
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if category is not None:
            updates.append("category = ?")
            params.append(category)
        if quantity is not None:
            updates.append("quantity = ?")
            params.append(quantity)
        if unit is not None:
            updates.append("unit = ?")
            params.append(unit)
        if supplier_id is not None:
            updates.append("supplier_id = ?")
            params.append(supplier_id)
        if purchase_date is not None:
            updates.append("purchase_date = ?")
            params.append(purchase_date)
        if photo_path is not None:
            updates.append("photo_path = ?")
            params.append(photo_path)
        
        if updates:
            params.append(item_id)
            query = f"UPDATE items SET {', '.join(updates)} WHERE id = ?"
            self.execute_query(query, tuple(params))

    def delete_item(self, item_id: int):
        """Delete an item by ID."""
        self.execute_query("DELETE FROM items WHERE id = ?", (item_id,))


class ProjectManager(BaseManager):
    def add_project(self, name: str, description: Optional[str] = None, date_created: Optional[str] = None) -> int:
        """Add a new project and return the project ID."""
        query = "INSERT INTO projects (name, description, date_created) VALUES (?, ?, ?)"
        return self.execute_query(query, (name, description, date_created))

    def get_project_by_id(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get a project by ID."""
        return self.fetch_one("SELECT * FROM projects WHERE id = ?", (project_id,))

    def get_all_projects(self) -> List[Dict[str, Any]]:
        """Get all projects."""
        return self.fetch_all("SELECT * FROM projects ORDER BY date_created DESC, name")

    def update_project(self, project_id: int, name: Optional[str] = None, description: Optional[str] = None,
                       date_created: Optional[str] = None):
        """Update a project. Only provided fields will be updated."""
        updates = []
        params = []
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if date_created is not None:
            updates.append("date_created = ?")
            params.append(date_created)
        
        if updates:
            params.append(project_id)
            query = f"UPDATE projects SET {', '.join(updates)} WHERE id = ?"
            self.execute_query(query, tuple(params))

    def delete_project(self, project_id: int):
        """Delete a project by ID."""
        self.execute_query("DELETE FROM projects WHERE id = ?", (project_id,))


class ProjectMaterialManager(BaseManager):
    def add_project_material(self, project_id: int, item_id: int, quantity_used: float) -> int:
        """Add a material to a project and return the material ID."""
        query = "INSERT INTO project_materials (project_id, item_id, quantity_used) VALUES (?, ?, ?)"
        return self.execute_query(query, (project_id, item_id, quantity_used))

    def get_materials_by_project(self, project_id: int) -> List[Dict[str, Any]]:
        """Get all materials for a project."""
        query = """SELECT pm.id, pm.project_id, pm.item_id, pm.quantity_used,
                          i.name as item_name, i.category, i.unit
                   FROM project_materials pm
                   JOIN items i ON pm.item_id = i.id
                   WHERE pm.project_id = ?
                   ORDER BY i.name"""
        return self.fetch_all(query, (project_id,))

    def update_project_material(self, material_id: int, item_id: Optional[int] = None, quantity_used: Optional[float] = None):
        """Update a project material. Only provided fields will be updated."""
        updates = []
        params = []
        if item_id is not None:
            updates.append("item_id = ?")
            params.append(item_id)
        if quantity_used is not None:
            updates.append("quantity_used = ?")
            params.append(quantity_used)
        
        if updates:
            params.append(material_id)
            query = f"UPDATE project_materials SET {', '.join(updates)} WHERE id = ?"
            self.execute_query(query, tuple(params))

    def delete_project_material(self, material_id: int):
        """Delete a project material by ID."""
        self.execute_query("DELETE FROM project_materials WHERE id = ?", (material_id,))
