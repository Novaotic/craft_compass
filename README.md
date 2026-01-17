# Craft Compass

Craft Compass is a lightweight inventory and tracking tool for DIY projects and craft materials. Built with simplicity and local-first architecture in mind, it uses SQLite and Python to manage your creative assets.

## Features

- Local database with schema-based initialization
- Simple query and fetch operations via db_manager.py
- Easy-to-run startup with main.py

## Getting Started
- Clone this repo:
```bash
git clone https://github.com/your-username/craft-compass.git
cd craft-compass
```
- Run the app:
```bash
python main.py
```

This will initialize your local craft_compass.db using the schema in database/schema.sql.

# Project Structure
craft-compass/
├── database/
│   ├── db_manager.py
│   └── schema.sql
├── models/
│   ├── item.py
│   ├── project.py
│   └── supplier.py
├── main.py
└── README.md

**Not included** - Current blank files for future project structure


## Requirements
- Python 3.10+
- SQLite (bundled with Python’s standard library)

# Roadmap (7/29/25)

## Phase 1 – Foundation
- ✅ Build out local schema and database operations
- ✅ Implement initialization logic in main.py
- ✅ Draft foundational documentation (README.md)
## Phase 2 – Core Functionality
- Create models to represent inventory items and categories
- Add insert/update/delete functionality to db_manager.py
- Develop basic CLI or GUI for user interaction
## Phase 3 – Enhancements
- Introduce search and filter capabilities
- Add support for tagging, images, or custom metadata
- Implement backups/export options (CSV or JSON)
## Phase 4 – Stretch Goals
- Web-based interface using Flask or FastAPI
- User authentication and multi-user support
- Option for cloud sync or remote storage


# Contributing

Thanks for considering a contribution to Craft Compass! Whether you're fixing bugs, improving docs, or adding new features, your input is always welcome.

## How to Contribute

- Fork the repository
    Use the GitHub “Fork” button to create your own copy.
- Create a feature branch
    Name your branch clearly:
```bash
git checkout -b feature/add-category-support
```
- Make your changes
    Keep your code modular, documented, and aligned with project structure.
- Run tests (if available)
    Ensure your changes don’t break anything.
- Submit a pull request
    Include a clear summary of the changes and reference any related issues.

## Contribution Guidelines

- Style: Follow Python’s PEP8 where applicable.
- Comments: Add brief docstrings and comments where necessary.
- Commits: Use descriptive commit messages.
- Issues: Tag your pull request with related issues to keep things linked and trackable.

## Communication

If you'd like to discuss an idea before implementing, feel free to open a GitHub issue or draft a pull request with a question. We welcome thoughtful collaboration.
