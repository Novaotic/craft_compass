# Craft Compass

Craft Compass is a lightweight inventory and tracking tool for DIY projects and craft materials. Built with simplicity and local-first architecture in mind, it uses SQLite and Python to manage your creative assets.

## Features

- **Local SQLite database** with schema-based initialization
- **Full CRUD operations** for items, projects, and suppliers
- **Graphical user interface** built with tkinter
- **Item management** with categories, quantities, units, and supplier tracking
- **Project tracking** with material usage and cost calculation
- **Inventory reports** with statistics and category breakdowns
- **Search and filter capabilities** across all entities with real-time filtering
- **Advanced tagging system** with many-to-many relationships for items and projects
- **Custom metadata support** for items with key-value pairs
- **Image management** with preview, validation, and automatic storage
- **Export/Import functionality** supporting CSV and JSON formats with conflict resolution
- **Easy-to-run startup** - just run `python main.py`

## Getting Started
- Clone this repo:
```bash
git clone https://github.com/your-username/craft-compass.git
cd craft-compass
```
- Install dependencies:
```bash
pip install -r requirements.txt
```

- Run the app:
```bash
python main.py
```

This will initialize your local `craft_compass.db` SQLite database using the schema in `database/schema.sql` and launch the graphical user interface.

## Usage

Once the application launches, you'll see a tabbed interface with four main sections:

- **Items**: Manage your inventory items - add items with categories, quantities, units, suppliers, purchase dates, tags, and images
- **Projects**: Create and track DIY projects, assign materials to projects, add tags, and monitor material usage
- **Suppliers**: Manage supplier information including contact details and notes
- **Reports**: View inventory statistics including total items, projects, suppliers, and category breakdowns

### Basic Workflow

1. **Add Suppliers**: Start by adding suppliers in the Suppliers tab
2. **Add Items**: Add inventory items in the Items tab, optionally linking them to suppliers, adding tags, and uploading images
3. **Create Projects**: Create projects in the Projects tab, assign materials from your inventory, and add tags
4. **View Reports**: Check the Reports tab for inventory statistics and insights
5. **Search and Filter**: Use the search bars and filter dropdowns in each tab to quickly find items, projects, or suppliers
6. **Manage Tags**: Use the "Tools > Manage Tags" menu to create, edit, and delete tags
7. **Export/Import**: Use "File > Export" to backup your data or "File > Import" to restore from a backup

### Advanced Features

- **Search**: Type in the search bar to find items, projects, or suppliers by name, category, or description
- **Filtering**: Use filter dropdowns to narrow results by category, supplier, date range, or quantity
- **Tagging**: Create tags and assign them to items and projects for better organization
- **Custom Metadata**: Add custom key-value pairs to items for additional information
- **Image Management**: Upload images for items with automatic validation and preview
- **Export/Import**: Export data to CSV (for spreadsheets) or JSON (for full backups), and import with conflict resolution options

All data is stored locally in the `craft_compass.db` SQLite database file in the project root directory. Images are stored in the `data/images/` directory.

## Testing

Craft Compass includes a comprehensive test suite using pytest. To run the tests:

```bash
# Install test dependencies (included in requirements.txt)
pip install -r requirements.txt

# Run all tests
pytest

# Run tests with coverage report
pytest --cov

# Run specific test file
pytest tests/test_models.py

# Run tests with verbose output
pytest -v
```

The test suite covers:
- **Database operations**: CRUD operations for items, projects, suppliers, materials, tags, and metadata
- **Models**: Item, Project, Supplier, and Tag model classes
- **Controllers**: Business logic and data flow
- **Validators**: Input validation functions
- **Helpers**: Utility functions
- **Search and Filter**: Search and filtering functionality across all entities
- **Tagging System**: Tag CRUD operations and associations with items and projects
- **Metadata**: Custom metadata CRUD operations
- **Export/Import**: CSV and JSON export/import functionality

Tests use temporary databases to ensure isolation and no interference with your actual data. Coverage reports are generated in HTML format in the `htmlcov/` directory.

# Project Structure
craft-compass/
├── database/
│   ├── database.py          # Database connection and initialization
│   ├── db_manager.py        # SQLite database operations (CRUD, search, filter, tags, metadata)
│   └── schema.sql        # Database schema definition
├── models/
│   ├── item.py             # Item model class
│   ├── project.py          # Project model class
│   ├── supplier.py         # Supplier model class
│   └── tag.py              # Tag model class
├── controllers/
│   ├── item_controllers.py # Item business logic
│   ├── project_controller.py # Project business logic
│   ├── report_controller.py # Report generation logic
│   ├── tag_controller.py   # Tag management logic
│   └── export_controller.py # Export/import logic
├── ui/
│   ├── main_window.py      # Main application window with menus and search/filter
│   ├── item_form.py        # Item creation/editing form with tags and image preview
│   ├── project_form.py     # Project creation/editing form with tags
│   ├── report_view.py      # Report display view
│   ├── search_filter_widget.py # Reusable search/filter component
│   ├── tag_manager.py      # Tag management dialog
│   ├── export_dialog.py   # Export dialog
│   ├── import_dialog.py    # Import dialog
│   └── metadata_form.py    # Metadata editor dialog
├── utils/
│   ├── helpers.py          # Utility functions
│   ├── validators.py       # Input validation functions
│   ├── export_service.py   # Export service (CSV/JSON)
│   ├── import_service.py   # Import service (CSV/JSON)
│   └── image_helpers.py    # Image management utilities
├── tests/
│   ├── __init__.py         # Test package initialization
│   ├── conftest.py         # Pytest fixtures and configuration
│   ├── test_db_manager.py  # Database operation tests
│   ├── test_models.py      # Model class tests
│   ├── test_controllers.py # Controller tests
│   ├── test_validators.py  # Validator function tests
│   ├── test_helpers.py     # Helper function tests
│   ├── test_search_filter.py # Search and filter tests
│   ├── test_tagging.py     # Tagging system tests
│   ├── test_metadata.py    # Metadata CRUD tests
│   └── test_export_import.py # Export/import tests
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── pytest.ini             # Pytest configuration
└── README.md              # This file


## Requirements
- Python 3.10+
- SQLite (bundled with Python’s standard library)

# Roadmap (7/29/25)

## Phase 1 – Foundation
- ✅ Build out local schema and database operations
- ✅ Implement initialization logic in main.py
- ✅ Draft foundational documentation (README.md)
## Phase 2 – Core Functionality
- ✅ Create models to represent inventory items and categories
- ✅ Add insert/update/delete functionality to db_manager.py
- ✅ Develop basic GUI for user interaction (tkinter-based interface)
## Phase 3 – Enhancements
- ✅ Introduce search and filter capabilities
- ✅ Add support for tagging, images, or custom metadata
- ✅ Implement backups/export options (CSV or JSON)
## Phase 4 – Stretch Goals
- Web-based interface using Flask or FastAPI
- User authentication and multi-user support
- Option for cloud sync or remote storage



