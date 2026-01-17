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
        # Enable foreign key constraints for cascade deletes
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def execute_query(self, query: str, params: tuple = ()):
        """Execute a query that modifies data (INSERT, UPDATE, DELETE)."""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            # Return lastrowid for INSERT operations
            return cursor.lastrowid
        finally:
            if conn:
                conn.close()
                del conn  # Explicitly delete to help with garbage collection

    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Fetch all rows from a query and return as list of dictionaries."""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            # Convert Row objects to dictionaries before closing connection
            result = [dict(row) for row in rows]
            return result
        finally:
            if conn:
                conn.close()
                del conn  # Explicitly delete to help with garbage collection

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """Fetch one row from a query and return as dictionary."""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            # Convert to dict before closing connection
            return dict(row) if row else None
        finally:
            if conn:
                conn.close()
                del conn  # Explicitly delete to help with garbage collection


class DatabaseAdmin(BaseManager):
    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.schema_path = SCHEMA_PATH

    def initialize_database(self):
        """Initialize the database with the schema."""
        conn = None
        try:
            conn = self.get_connection()
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
        finally:
            if conn:
                conn.close()
                del conn  # Explicitly delete to help with garbage collection

    def reset_database(self):
        """Drop all tables and reinitialize the database."""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table['name']};")
            conn.commit()
        finally:
            if conn:
                conn.close()
                del conn  # Explicitly delete to help with garbage collection
        
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
    
    def search_suppliers(self, search_term: str) -> List[Dict[str, Any]]:
        """Search suppliers by name or contact info."""
        search_pattern = f"%{search_term}%"
        query = """SELECT * FROM suppliers 
                   WHERE name LIKE ? OR contact_info LIKE ? OR website LIKE ? OR notes LIKE ?
                   ORDER BY name"""
        return self.fetch_all(query, (search_pattern, search_pattern, search_pattern, search_pattern))


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
    
    def search_items(self, search_term: str) -> List[Dict[str, Any]]:
        """Search items by name, category, or supplier name."""
        search_pattern = f"%{search_term}%"
        query = """SELECT i.* FROM items i
                   LEFT JOIN suppliers s ON i.supplier_id = s.id
                   WHERE i.name LIKE ? OR i.category LIKE ? OR s.name LIKE ?
                   ORDER BY i.name"""
        return self.fetch_all(query, (search_pattern, search_pattern, search_pattern))
    
    def filter_items(self, category: Optional[str] = None, supplier_id: Optional[int] = None,
                     date_from: Optional[str] = None, date_to: Optional[str] = None,
                     quantity_min: Optional[float] = None, quantity_max: Optional[float] = None) -> List[Dict[str, Any]]:
        """Filter items by various criteria."""
        conditions = []
        params = []
        
        if category:
            conditions.append("category = ?")
            params.append(category)
        if supplier_id is not None:
            conditions.append("supplier_id = ?")
            params.append(supplier_id)
        if date_from:
            conditions.append("purchase_date >= ?")
            params.append(date_from)
        if date_to:
            conditions.append("purchase_date <= ?")
            params.append(date_to)
        if quantity_min is not None:
            conditions.append("quantity >= ?")
            params.append(quantity_min)
        if quantity_max is not None:
            conditions.append("quantity <= ?")
            params.append(quantity_max)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        query = f"SELECT * FROM items WHERE {where_clause} ORDER BY name"
        return self.fetch_all(query, tuple(params))
    
    def add_metadata(self, item_id: int, key: str, value: str):
        """Add or update metadata for an item."""
        query = """INSERT INTO item_metadata (item_id, key, value) 
                   VALUES (?, ?, ?)
                   ON CONFLICT(item_id, key) DO UPDATE SET value = excluded.value"""
        self.execute_query(query, (item_id, key, value))
    
    def get_metadata(self, item_id: int, key: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get metadata for an item. If key is provided, get specific metadata."""
        if key:
            return self.fetch_all("SELECT * FROM item_metadata WHERE item_id = ? AND key = ?", (item_id, key))
        return self.fetch_all("SELECT * FROM item_metadata WHERE item_id = ?", (item_id,))
    
    def update_metadata(self, item_id: int, key: str, value: str):
        """Update metadata for an item (same as add_metadata due to ON CONFLICT)."""
        self.add_metadata(item_id, key, value)
    
    def delete_metadata(self, item_id: int, key: Optional[str] = None):
        """Delete metadata for an item. If key is provided, delete specific metadata."""
        if key:
            self.execute_query("DELETE FROM item_metadata WHERE item_id = ? AND key = ?", (item_id, key))
        else:
            self.execute_query("DELETE FROM item_metadata WHERE item_id = ?", (item_id,))


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
    
    def search_projects(self, search_term: str) -> List[Dict[str, Any]]:
        """Search projects by name or description."""
        search_pattern = f"%{search_term}%"
        query = """SELECT * FROM projects 
                   WHERE name LIKE ? OR description LIKE ?
                   ORDER BY date_created DESC, name"""
        return self.fetch_all(query, (search_pattern, search_pattern))
    
    def filter_projects(self, date_from: Optional[str] = None, date_to: Optional[str] = None,
                       min_materials: Optional[int] = None) -> List[Dict[str, Any]]:
        """Filter projects by date range or material count."""
        conditions = []
        params = []
        
        if date_from:
            conditions.append("date_created >= ?")
            params.append(date_from)
        if date_to:
            conditions.append("date_created <= ?")
            params.append(date_to)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        if min_materials is not None:
            # Use subquery to count materials
            query = f"""SELECT p.* FROM projects p
                       LEFT JOIN project_materials pm ON p.id = pm.project_id
                       WHERE {where_clause}
                       GROUP BY p.id
                       HAVING COUNT(pm.id) >= ?
                       ORDER BY p.date_created DESC, p.name"""
            params.append(min_materials)
        else:
            query = f"SELECT * FROM projects WHERE {where_clause} ORDER BY date_created DESC, name"
        
        return self.fetch_all(query, tuple(params))


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


class TagManager(BaseManager):
    def add_tag(self, name: str, color: Optional[str] = None) -> int:
        """Add a new tag and return the tag ID."""
        query = "INSERT INTO tags (name, color) VALUES (?, ?)"
        return self.execute_query(query, (name, color))
    
    def get_tag_by_id(self, tag_id: int) -> Optional[Dict[str, Any]]:
        """Get a tag by ID."""
        return self.fetch_one("SELECT * FROM tags WHERE id = ?", (tag_id,))
    
    def get_tag_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a tag by name."""
        return self.fetch_one("SELECT * FROM tags WHERE name = ?", (name,))
    
    def get_all_tags(self) -> List[Dict[str, Any]]:
        """Get all tags."""
        return self.fetch_all("SELECT * FROM tags ORDER BY name")
    
    def update_tag(self, tag_id: int, name: Optional[str] = None, color: Optional[str] = None):
        """Update a tag. Only provided fields will be updated."""
        updates = []
        params = []
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if color is not None:
            updates.append("color = ?")
            params.append(color)
        
        if updates:
            params.append(tag_id)
            query = f"UPDATE tags SET {', '.join(updates)} WHERE id = ?"
            self.execute_query(query, tuple(params))
    
    def delete_tag(self, tag_id: int):
        """Delete a tag by ID (cascade deletes associations)."""
        self.execute_query("DELETE FROM tags WHERE id = ?", (tag_id,))
    
    def add_tag_to_item(self, item_id: int, tag_id: int):
        """Associate a tag with an item."""
        query = "INSERT OR IGNORE INTO item_tags (item_id, tag_id) VALUES (?, ?)"
        self.execute_query(query, (item_id, tag_id))
    
    def remove_tag_from_item(self, item_id: int, tag_id: int):
        """Remove a tag association from an item."""
        query = "DELETE FROM item_tags WHERE item_id = ? AND tag_id = ?"
        self.execute_query(query, (item_id, tag_id))
    
    def get_item_tags(self, item_id: int) -> List[Dict[str, Any]]:
        """Get all tags for an item."""
        query = """SELECT t.* FROM tags t
                   JOIN item_tags it ON t.id = it.tag_id
                   WHERE it.item_id = ?
                   ORDER BY t.name"""
        return self.fetch_all(query, (item_id,))
    
    def add_tag_to_project(self, project_id: int, tag_id: int):
        """Associate a tag with a project."""
        query = "INSERT OR IGNORE INTO project_tags (project_id, tag_id) VALUES (?, ?)"
        self.execute_query(query, (project_id, tag_id))
    
    def remove_tag_from_project(self, project_id: int, tag_id: int):
        """Remove a tag association from a project."""
        query = "DELETE FROM project_tags WHERE project_id = ? AND tag_id = ?"
        self.execute_query(query, (project_id, tag_id))
    
    def get_project_tags(self, project_id: int) -> List[Dict[str, Any]]:
        """Get all tags for a project."""
        query = """SELECT t.* FROM tags t
                   JOIN project_tags pt ON t.id = pt.tag_id
                   WHERE pt.project_id = ?
                   ORDER BY t.name"""
        return self.fetch_all(query, (project_id,))
    
    def get_items_by_tag(self, tag_id: int) -> List[Dict[str, Any]]:
        """Get all items with a specific tag."""
        query = """SELECT i.* FROM items i
                   JOIN item_tags it ON i.id = it.item_id
                   WHERE it.tag_id = ?
                   ORDER BY i.name"""
        return self.fetch_all(query, (tag_id,))
    
    def get_projects_by_tag(self, tag_id: int) -> List[Dict[str, Any]]:
        """Get all projects with a specific tag."""
        query = """SELECT p.* FROM projects p
                   JOIN project_tags pt ON p.id = pt.project_id
                   WHERE pt.tag_id = ?
                   ORDER BY p.date_created DESC, p.name"""
        return self.fetch_all(query, (tag_id,))
