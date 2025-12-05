"""
Database module for Home Library application.
Handles SQLite connection and table initialization.
"""
import sqlite3
import os
from pathlib import Path


def get_db_path() -> str:
    """Get the path to the database file."""
    return str(Path(__file__).parent / "library.db")


def get_connection() -> sqlite3.Connection:
    """Get a database connection with row factory."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_database():
    """Initialize the database with all required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Publication Types table (Науково-технічне, Підручник, Художня література)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS publication_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    
    # Genres table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    
    # Authors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    
    # Storage Locations table (cabinet, shelf)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS storage_locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cabinet TEXT NOT NULL,
            shelf TEXT NOT NULL,
            UNIQUE(cabinet, shelf)
        )
    """)
    
    # Publications table (books and periodicals)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS publications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            publication_kind TEXT NOT NULL CHECK(publication_kind IN ('book', 'periodical')),
            year INTEGER,
            publication_type_id INTEGER,
            storage_location_id INTEGER,
            FOREIGN KEY (publication_type_id) REFERENCES publication_types(id) ON DELETE SET NULL,
            FOREIGN KEY (storage_location_id) REFERENCES storage_locations(id) ON DELETE SET NULL
        )
    """)
    
    # Publication-Authors junction table (many-to-many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS publication_authors (
            publication_id INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            PRIMARY KEY (publication_id, author_id),
            FOREIGN KEY (publication_id) REFERENCES publications(id) ON DELETE CASCADE,
            FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
        )
    """)
    
    # Publication-Genres junction table (many-to-many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS publication_genres (
            publication_id INTEGER NOT NULL,
            genre_id INTEGER NOT NULL,
            PRIMARY KEY (publication_id, genre_id),
            FOREIGN KEY (publication_id) REFERENCES publications(id) ON DELETE CASCADE,
            FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
        )
    """)
    
    # Insert default publication types if not exist
    default_types = [
        "Науково-технічне",
        "Підручник", 
        "Художня література"
    ]
    for type_name in default_types:
        cursor.execute(
            "INSERT OR IGNORE INTO publication_types (name) VALUES (?)",
            (type_name,)
        )
    
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully!")
