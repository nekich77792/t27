"""
Search functions for Home Library application.
Contains search and query operations.
"""
from typing import List
from database import get_connection
from .classes import Author, Genre, PublicationType, StorageLocation, Publication


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
