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

-- Table: tags
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    color TEXT
);

-- Table: item_tags (many-to-many relationship)
CREATE TABLE IF NOT EXISTS item_tags (
    item_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (item_id, tag_id),
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Table: project_tags (many-to-many relationship)
CREATE TABLE IF NOT EXISTS project_tags (
    project_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (project_id, tag_id),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Table: item_metadata (key-value store for custom metadata)
CREATE TABLE IF NOT EXISTS item_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    UNIQUE(item_id, key)
);
