"""
Models and data access layer for Home Library application.
Contains CRUD operations for all entities.
"""
from dataclasses import dataclass
from typing import List, Optional
from database import get_connection


# ============== Data Classes ==============

@dataclass
class Author:
    id: Optional[int]
    name: str


@dataclass
class Genre:
    id: Optional[int]
    name: str


@dataclass
class PublicationType:
    id: Optional[int]
    name: str


@dataclass
class StorageLocation:
    id: Optional[int]
    cabinet: str
    shelf: str
    
    def __str__(self):
        return f"Шафа: {self.cabinet}, Полиця: {self.shelf}"


@dataclass
class Publication:
    id: Optional[int]
    title: str
    publication_kind: str  # 'book' or 'periodical'
    year: Optional[int]
    publication_type_id: Optional[int]
    storage_location_id: Optional[int]
    authors: List[Author] = None
    genres: List[Genre] = None
    publication_type: Optional[PublicationType] = None
    storage_location: Optional[StorageLocation] = None
    
    def __post_init__(self):
        if self.authors is None:
            self.authors = []
        if self.genres is None:
            self.genres = []


# ============== Author CRUD ==============

def get_all_authors() -> List[Author]:
    conn = get_connection()
    cursor = conn.execute("SELECT id, name FROM authors ORDER BY name")
    authors = [Author(id=row['id'], name=row['name']) for row in cursor.fetchall()]
    conn.close()
    return authors


def get_author_by_id(author_id: int) -> Optional[Author]:
    conn = get_connection()
    cursor = conn.execute("SELECT id, name FROM authors WHERE id = ?", (author_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Author(id=row['id'], name=row['name'])
    return None


def create_author(name: str) -> int:
    conn = get_connection()
    cursor = conn.execute("INSERT INTO authors (name) VALUES (?)", (name,))
    author_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return author_id


def update_author(author_id: int, name: str):
    conn = get_connection()
    conn.execute("UPDATE authors SET name = ? WHERE id = ?", (name, author_id))
    conn.commit()
    conn.close()


def delete_author(author_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM authors WHERE id = ?", (author_id,))
    conn.commit()
    conn.close()


# ============== Genre CRUD ==============

def get_all_genres() -> List[Genre]:
    conn = get_connection()
    cursor = conn.execute("SELECT id, name FROM genres ORDER BY name")
    genres = [Genre(id=row['id'], name=row['name']) for row in cursor.fetchall()]
    conn.close()
    return genres


def get_genre_by_id(genre_id: int) -> Optional[Genre]:
    conn = get_connection()
    cursor = conn.execute("SELECT id, name FROM genres WHERE id = ?", (genre_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Genre(id=row['id'], name=row['name'])
    return None


def create_genre(name: str) -> int:
    conn = get_connection()
    cursor = conn.execute("INSERT INTO genres (name) VALUES (?)", (name,))
    genre_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return genre_id


def update_genre(genre_id: int, name: str):
    conn = get_connection()
    conn.execute("UPDATE genres SET name = ? WHERE id = ?", (name, genre_id))
    conn.commit()
    conn.close()


def delete_genre(genre_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM genres WHERE id = ?", (genre_id,))
    conn.commit()
    conn.close()


# ============== Publication Type CRUD ==============

def get_all_publication_types() -> List[PublicationType]:
    conn = get_connection()
    cursor = conn.execute("SELECT id, name FROM publication_types ORDER BY name")
    types = [PublicationType(id=row['id'], name=row['name']) for row in cursor.fetchall()]
    conn.close()
    return types


def get_publication_type_by_id(type_id: int) -> Optional[PublicationType]:
    conn = get_connection()
    cursor = conn.execute("SELECT id, name FROM publication_types WHERE id = ?", (type_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return PublicationType(id=row['id'], name=row['name'])
    return None


def create_publication_type(name: str) -> int:
    conn = get_connection()
    cursor = conn.execute("INSERT INTO publication_types (name) VALUES (?)", (name,))
    type_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return type_id


def update_publication_type(type_id: int, name: str):
    conn = get_connection()
    conn.execute("UPDATE publication_types SET name = ? WHERE id = ?", (name, type_id))
    conn.commit()
    conn.close()


def delete_publication_type(type_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM publication_types WHERE id = ?", (type_id,))
    conn.commit()
    conn.close()


# ============== Storage Location CRUD ==============

def get_all_storage_locations() -> List[StorageLocation]:
    conn = get_connection()
    cursor = conn.execute("SELECT id, cabinet, shelf FROM storage_locations ORDER BY cabinet, shelf")
    locations = [StorageLocation(id=row['id'], cabinet=row['cabinet'], shelf=row['shelf']) 
                 for row in cursor.fetchall()]
    conn.close()
    return locations


def get_storage_location_by_id(location_id: int) -> Optional[StorageLocation]:
    conn = get_connection()
    cursor = conn.execute("SELECT id, cabinet, shelf FROM storage_locations WHERE id = ?", (location_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return StorageLocation(id=row['id'], cabinet=row['cabinet'], shelf=row['shelf'])
    return None


def create_storage_location(cabinet: str, shelf: str) -> int:
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO storage_locations (cabinet, shelf) VALUES (?, ?)",
        (cabinet, shelf)
    )
    location_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return location_id


def update_storage_location(location_id: int, cabinet: str, shelf: str):
    conn = get_connection()
    conn.execute(
        "UPDATE storage_locations SET cabinet = ?, shelf = ? WHERE id = ?",
        (cabinet, shelf, location_id)
    )
    conn.commit()
    conn.close()


def delete_storage_location(location_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM storage_locations WHERE id = ?", (location_id,))
    conn.commit()
    conn.close()


# ============== Publication CRUD ==============

def get_all_publications() -> List[Publication]:
    conn = get_connection()
    cursor = conn.execute("""
        SELECT p.id, p.title, p.publication_kind, p.year, 
               p.publication_type_id, p.storage_location_id,
               pt.name as type_name,
               sl.cabinet, sl.shelf
        FROM publications p
        LEFT JOIN publication_types pt ON p.publication_type_id = pt.id
        LEFT JOIN storage_locations sl ON p.storage_location_id = sl.id
        ORDER BY p.title
    """)
    
    publications = []
    for row in cursor.fetchall():
        pub = Publication(
            id=row['id'],
            title=row['title'],
            publication_kind=row['publication_kind'],
            year=row['year'],
            publication_type_id=row['publication_type_id'],
            storage_location_id=row['storage_location_id']
        )
        
        if row['type_name']:
            pub.publication_type = PublicationType(
                id=row['publication_type_id'],
                name=row['type_name']
            )
        
        if row['cabinet']:
            pub.storage_location = StorageLocation(
                id=row['storage_location_id'],
                cabinet=row['cabinet'],
                shelf=row['shelf']
            )
        
        # Load authors
        author_cursor = conn.execute("""
            SELECT a.id, a.name
            FROM authors a
            JOIN publication_authors pa ON a.id = pa.author_id
            WHERE pa.publication_id = ?
        """, (pub.id,))
        pub.authors = [Author(id=r['id'], name=r['name']) for r in author_cursor.fetchall()]
        
        # Load genres
        genre_cursor = conn.execute("""
            SELECT g.id, g.name
            FROM genres g
            JOIN publication_genres pg ON g.id = pg.genre_id
            WHERE pg.publication_id = ?
        """, (pub.id,))
        pub.genres = [Genre(id=r['id'], name=r['name']) for r in genre_cursor.fetchall()]
        
        publications.append(pub)
    
    conn.close()
    return publications


def get_publication_by_id(publication_id: int) -> Optional[Publication]:
    conn = get_connection()
    cursor = conn.execute("""
        SELECT p.id, p.title, p.publication_kind, p.year,
               p.publication_type_id, p.storage_location_id
        FROM publications p
        WHERE p.id = ?
    """, (publication_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return None
    
    pub = Publication(
        id=row['id'],
        title=row['title'],
        publication_kind=row['publication_kind'],
        year=row['year'],
        publication_type_id=row['publication_type_id'],
        storage_location_id=row['storage_location_id']
    )
    
    # Load authors
    author_cursor = conn.execute("""
        SELECT a.id, a.name
        FROM authors a
        JOIN publication_authors pa ON a.id = pa.author_id
        WHERE pa.publication_id = ?
    """, (pub.id,))
    pub.authors = [Author(id=r['id'], name=r['name']) for r in author_cursor.fetchall()]
    
    # Load genres
    genre_cursor = conn.execute("""
        SELECT g.id, g.name
        FROM genres g
        JOIN publication_genres pg ON g.id = pg.genre_id
        WHERE pg.publication_id = ?
    """, (pub.id,))
    pub.genres = [Genre(id=r['id'], name=r['name']) for r in genre_cursor.fetchall()]
    
    conn.close()
    return pub


def create_publication(title: str, publication_kind: str, year: Optional[int],
                       publication_type_id: Optional[int], storage_location_id: Optional[int],
                       author_ids: List[int], genre_ids: List[int]) -> int:
    conn = get_connection()
    cursor = conn.execute("""
        INSERT INTO publications (title, publication_kind, year, publication_type_id, storage_location_id)
        VALUES (?, ?, ?, ?, ?)
    """, (title, publication_kind, year, publication_type_id, storage_location_id))
    publication_id = cursor.lastrowid
    
    # Link authors
    for author_id in author_ids:
        conn.execute(
            "INSERT INTO publication_authors (publication_id, author_id) VALUES (?, ?)",
            (publication_id, author_id)
        )
    
    # Link genres
    for genre_id in genre_ids:
        conn.execute(
            "INSERT INTO publication_genres (publication_id, genre_id) VALUES (?, ?)",
            (publication_id, genre_id)
        )
    
    conn.commit()
    conn.close()
    return publication_id


def update_publication(publication_id: int, title: str, publication_kind: str, 
                       year: Optional[int], publication_type_id: Optional[int],
                       storage_location_id: Optional[int],
                       author_ids: List[int], genre_ids: List[int]):
    conn = get_connection()
    conn.execute("""
        UPDATE publications 
        SET title = ?, publication_kind = ?, year = ?, 
            publication_type_id = ?, storage_location_id = ?
        WHERE id = ?
    """, (title, publication_kind, year, publication_type_id, storage_location_id, publication_id))
    
    # Update authors - remove old, add new
    conn.execute("DELETE FROM publication_authors WHERE publication_id = ?", (publication_id,))
    for author_id in author_ids:
        conn.execute(
            "INSERT INTO publication_authors (publication_id, author_id) VALUES (?, ?)",
            (publication_id, author_id)
        )
    
    # Update genres - remove old, add new
    conn.execute("DELETE FROM publication_genres WHERE publication_id = ?", (publication_id,))
    for genre_id in genre_ids:
        conn.execute(
            "INSERT INTO publication_genres (publication_id, genre_id) VALUES (?, ?)",
            (publication_id, genre_id)
        )
    
    conn.commit()
    conn.close()


def delete_publication(publication_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM publications WHERE id = ?", (publication_id,))
    conn.commit()
    conn.close()


# ============== Search Functions ==============

def search_publications(title: str = None, author_id: int = None, 
                        genre_id: int = None, type_id: int = None) -> List[Publication]:
    """Search publications by various criteria."""
    conn = get_connection()
    
    query = """
        SELECT DISTINCT p.id, p.title, p.publication_kind, p.year,
               p.publication_type_id, p.storage_location_id,
               pt.name as type_name,
               sl.cabinet, sl.shelf
        FROM publications p
        LEFT JOIN publication_types pt ON p.publication_type_id = pt.id
        LEFT JOIN storage_locations sl ON p.storage_location_id = sl.id
        LEFT JOIN publication_authors pa ON p.id = pa.publication_id
        LEFT JOIN publication_genres pg ON p.id = pg.publication_id
        WHERE 1=1
    """
    params = []
    
    if title:
        query += " AND p.title LIKE ?"
        params.append(f"%{title}%")
    
    if author_id:
        query += " AND pa.author_id = ?"
        params.append(author_id)
    
    if genre_id:
        query += " AND pg.genre_id = ?"
        params.append(genre_id)
    
    if type_id:
        query += " AND p.publication_type_id = ?"
        params.append(type_id)
    
    query += " ORDER BY p.title"
    
    cursor = conn.execute(query, params)
    
    publications = []
    for row in cursor.fetchall():
        pub = Publication(
            id=row['id'],
            title=row['title'],
            publication_kind=row['publication_kind'],
            year=row['year'],
            publication_type_id=row['publication_type_id'],
            storage_location_id=row['storage_location_id']
        )
        
        if row['type_name']:
            pub.publication_type = PublicationType(
                id=row['publication_type_id'],
                name=row['type_name']
            )
        
        if row['cabinet']:
            pub.storage_location = StorageLocation(
                id=row['storage_location_id'],
                cabinet=row['cabinet'],
                shelf=row['shelf']
            )
        
        # Load authors
        author_cursor = conn.execute("""
            SELECT a.id, a.name
            FROM authors a
            JOIN publication_authors pa ON a.id = pa.author_id
            WHERE pa.publication_id = ?
        """, (pub.id,))
        pub.authors = [Author(id=r['id'], name=r['name']) for r in author_cursor.fetchall()]
        
        # Load genres
        genre_cursor = conn.execute("""
            SELECT g.id, g.name
            FROM genres g
            JOIN publication_genres pg ON g.id = pg.genre_id
            WHERE pg.publication_id = ?
        """, (pub.id,))
        pub.genres = [Genre(id=r['id'], name=r['name']) for r in genre_cursor.fetchall()]
        
        publications.append(pub)
    
    conn.close()
    return publications
