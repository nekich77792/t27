"""
Search view for Home Library application.
"""
import tkinter as tk
from tkinter import ttk
import models


class SearchView(ttk.Frame):
    """Frame for searching publications."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI components."""
        # Title
        title_label = ttk.Label(self, text="Пошук видань", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(10, 5))
        
        # Search form
        search_frame = ttk.LabelFrame(self, text="Параметри пошуку", padding=10)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        # Load reference data
        self.all_authors = models.get_all_authors()
        self.all_genres = models.get_all_genres()
        self.all_types = models.get_all_publication_types()
        
        # Title search
        ttk.Label(search_frame, text="Назва:").grid(row=0, column=0, sticky='w', pady=3, padx=5)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(search_frame, textvariable=self.title_var, width=30)
        self.title_entry.grid(row=0, column=1, sticky='w', pady=3)
        
        # Author filter
        ttk.Label(search_frame, text="Автор:").grid(row=0, column=2, sticky='w', pady=3, padx=(20, 5))
        self.author_var = tk.StringVar()
        author_values = ["-- Всі автори --"] + [a.name for a in self.all_authors]
        self.author_combo = ttk.Combobox(search_frame, textvariable=self.author_var, 
                                          values=author_values, state='readonly', width=25)
        self.author_combo.current(0)
        self.author_combo.grid(row=0, column=3, sticky='w', pady=3)
        
        # Genre filter
        ttk.Label(search_frame, text="Жанр:").grid(row=1, column=0, sticky='w', pady=3, padx=5)
        self.genre_var = tk.StringVar()
        genre_values = ["-- Всі жанри --"] + [g.name for g in self.all_genres]
        self.genre_combo = ttk.Combobox(search_frame, textvariable=self.genre_var,
                                         values=genre_values, state='readonly', width=25)
        self.genre_combo.current(0)
        self.genre_combo.grid(row=1, column=1, sticky='w', pady=3)
        
        # Type filter
        ttk.Label(search_frame, text="Вид:").grid(row=1, column=2, sticky='w', pady=3, padx=(20, 5))
        self.type_var = tk.StringVar()
        type_values = ["-- Всі види --"] + [t.name for t in self.all_types]
        self.type_combo = ttk.Combobox(search_frame, textvariable=self.type_var,
                                        values=type_values, state='readonly', width=25)
        self.type_combo.current(0)
        self.type_combo.grid(row=1, column=3, sticky='w', pady=3)
        
        # Buttons
        btn_frame = ttk.Frame(search_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=(10, 0))
        
        ttk.Button(btn_frame, text="🔍 Шукати", command=self.search).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔄 Скинути", command=self.reset).pack(side='left', padx=5)
        
        # Bind Enter key to search
        self.title_entry.bind('<Return>', lambda e: self.search())
        
        # Results section
        results_frame = ttk.LabelFrame(self, text="Результати пошуку", padding=5)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Results count
        self.results_label = ttk.Label(results_frame, text="Введіть критерії пошуку та натисніть 'Шукати'")
        self.results_label.pack(anchor='w', pady=5)
        
        # Results treeview
        tree_frame = ttk.Frame(results_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('title', 'kind', 'authors', 'genres', 'type', 'year', 'location')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        self.tree.heading('title', text='Назва')
        self.tree.heading('kind', text='Тип')
        self.tree.heading('authors', text='Автор(и)')
        self.tree.heading('genres', text='Жанр(и)')
        self.tree.heading('type', text='Вид')
        self.tree.heading('year', text='Рік')
        self.tree.heading('location', text='Місце')
        
        self.tree.column('title', width=200)
        self.tree.column('kind', width=80)
        self.tree.column('authors', width=150)
        self.tree.column('genres', width=120)
        self.tree.column('type', width=120)
        self.tree.column('year', width=50, anchor='center')
        self.tree.column('location', width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def refresh_dropdowns(self):
        """Refresh dropdown values with latest data."""
        self.all_authors = models.get_all_authors()
        self.all_genres = models.get_all_genres()
        self.all_types = models.get_all_publication_types()
        
        self.author_combo['values'] = ["-- Всі автори --"] + [a.name for a in self.all_authors]
        self.genre_combo['values'] = ["-- Всі жанри --"] + [g.name for g in self.all_genres]
        self.type_combo['values'] = ["-- Всі види --"] + [t.name for t in self.all_types]
    
    def search(self):
        """Perform search with current criteria."""
        # Refresh dropdowns in case data changed
        self.refresh_dropdowns()
        
        # Get search parameters
        title = self.title_var.get().strip() or None
        
        # Get author ID
        author_id = None
        author_name = self.author_var.get()
        if author_name and not author_name.startswith("--"):
            for a in self.all_authors:
                if a.name == author_name:
                    author_id = a.id
                    break
        
        # Get genre ID
        genre_id = None
        genre_name = self.genre_var.get()
        if genre_name and not genre_name.startswith("--"):
            for g in self.all_genres:
                if g.name == genre_name:
                    genre_id = g.id
                    break
        
        # Get type ID
        type_id = None
        type_name = self.type_var.get()
        if type_name and not type_name.startswith("--"):
            for t in self.all_types:
                if t.name == type_name:
                    type_id = t.id
                    break
        
        # Perform search
        results = models.search_publications(
            title=title,
            author_id=author_id,
            genre_id=genre_id,
            type_id=type_id
        )
        
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Display results
        self.results_label.config(text=f"Знайдено видань: {len(results)}")
        
        for pub in results:
            kind_display = "📚 Книга" if pub.publication_kind == 'book' else "📰 Періодика"
            authors = ", ".join([a.name for a in pub.authors]) if pub.authors else "-"
            genres = ", ".join([g.name for g in pub.genres]) if pub.genres else "-"
            pub_type = pub.publication_type.name if pub.publication_type else "-"
            year = pub.year if pub.year else "-"
            location = str(pub.storage_location) if pub.storage_location else "-"
            
            self.tree.insert('', 'end', values=(
                pub.title, kind_display, authors, genres, pub_type, year, location
            ))
    
    def reset(self):
        """Reset all search criteria."""
        self.title_var.set("")
        self.author_combo.current(0)
        self.genre_combo.current(0)
        self.type_combo.current(0)
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.results_label.config(text="Введіть критерії пошуку та натисніть 'Шукати'")
