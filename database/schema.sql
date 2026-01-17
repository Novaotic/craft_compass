-- Table: suppliers
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_info TEXT NOT NULL,
    website TEXT,
    notes TEXT
);

-- Table: items
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    quantity REAL,
    unit TEXT,
    supplier_id INTEGER,
    purchase_date TEXT,
    photo_path TEXT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

-- Table: projects
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    date_created TEXT
);

-- Table: project_materials
CREATE TABLE IF NOT EXISTS project_materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    item_id INTEGER,
    quantity_used REAL,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (item_id) REFERENCES items(id)
);
