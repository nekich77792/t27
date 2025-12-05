"""
Data classes for Home Library application.
Contains all entity definitions.
"""
from dataclasses import dataclass
from typing import List, Optional


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
