# Craft Compass

Craft Compass is a lightweight inventory and tracking tool for DIY projects and craft materials. Built with simplicity and local-first architecture in mind, it uses SQLite and Python to manage your creative assets.

## Features

- **Local SQLite database** with schema-based initialization
- **Full CRUD operations** for items, projects, and suppliers
- **Graphical user interface** built with tkinter
- **Item management** with categories, quantities, units, and supplier tracking
- **Project tracking** with material usage and cost calculation
- **Inventory reports** with statistics and category breakdowns
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

- **Items**: Manage your inventory items - add items with categories, quantities, units, suppliers, and purchase dates
- **Projects**: Create and track DIY projects, assign materials to projects, and monitor material usage
- **Suppliers**: Manage supplier information including contact details and notes
- **Reports**: View inventory statistics including total items, projects, suppliers, and category breakdowns

### Basic Workflow

1. **Add Suppliers**: Start by adding suppliers in the Suppliers tab
2. **Add Items**: Add inventory items in the Items tab, optionally linking them to suppliers
3. **Create Projects**: Create projects in the Projects tab and assign materials from your inventory
4. **View Reports**: Check the Reports tab for inventory statistics and insights

All data is stored locally in the `craft_compass.db` SQLite database file in the project root directory.

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
- **Database operations**: CRUD operations for items, projects, suppliers, and materials
- **Models**: Item, Project, and Supplier model classes
- **Controllers**: Business logic and data flow
- **Validators**: Input validation functions
- **Helpers**: Utility functions

Tests use temporary databases to ensure isolation and no interference with your actual data. Coverage reports are generated in HTML format in the `htmlcov/` directory.

# Project Structure
craft-compass/
├── database/
│   ├── database.py          # Database connection and initialization
│   ├── db_manager.py        # SQLite database operations (CRUD)
│   └── schema.sql           # Database schema definition
├── models/
│   ├── item.py              # Item model class
│   ├── project.py           # Project model class
│   └── supplier.py          # Supplier model class
├── controllers/
│   ├── item_controllers.py  # Item business logic
│   ├── project_controller.py # Project business logic
│   └── report_controller.py  # Report generation logic
├── ui/
│   ├── main_window.py       # Main application window
│   ├── item_form.py         # Item creation/editing form
│   ├── project_form.py      # Project creation/editing form
│   └── report_view.py       # Report display view
├── utils/
│   ├── helpers.py           # Utility functions
│   └── validators.py        # Input validation functions
├── tests/
│   ├── __init__.py          # Test package initialization
│   ├── conftest.py          # Pytest fixtures and configuration
│   ├── test_db_manager.py   # Database operation tests
│   ├── test_models.py       # Model class tests
│   ├── test_controllers.py  # Controller tests
│   ├── test_validators.py   # Validator function tests
│   └── test_helpers.py      # Helper function tests
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── pytest.ini              # Pytest configuration
└── README.md                # This file


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
- Introduce search and filter capabilities
- Add support for tagging, images, or custom metadata
- Implement backups/export options (CSV or JSON)
## Phase 4 – Stretch Goals
- Web-based interface using Flask or FastAPI
- User authentication and multi-user support
- Option for cloud sync or remote storage



