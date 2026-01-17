"""Main entry point for Craft Compass application."""
from database.database import CraftCompassDB
from ui.main_window import MainWindow


def main():
    """Initialize database and launch GUI."""
    print("Craft Compass is starting...")

    # Initialize database
    db = CraftCompassDB()
    db.initialize()

    print("Database initialized. Launching GUI...")

    # Launch GUI
    app = MainWindow(db)
    app.run()

    print("Craft Compass is closing. Goodbye!")


if __name__ == "__main__":
    main()
