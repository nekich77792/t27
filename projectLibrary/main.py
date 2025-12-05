"""
Home Library Application - Домашня Бібліотека
Main entry point for the application.
"""
import sys
import os

# Add the project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_database
from ui.main_window import create_main_window


def main():
    """Main application entry point."""
    # Initialize the database (creates tables if not exist)
    print("Initializing database...")
    init_database()
    print("Database ready!")
    
    # Create and run the main window
    print("Starting application...")
    root = create_main_window()
    root.mainloop()


if __name__ == "__main__":
    main()
