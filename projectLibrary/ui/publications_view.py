"""
Publications management view for Home Library application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import models


class PublicationsView(ttk.Frame):
    """Frame for managing publications (books and periodicals)."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup the UI components."""
        # Title
        title_label = ttk.Label(self, text="Видання", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(10, 5))
        
        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(toolbar, text="➕ Додати", command=self.add_publication).pack(side='left', padx=2)
        ttk.Button(toolbar, text="✏️ Редагувати", command=self.edit_publication).pack(side='left', padx=2)
        ttk.Button(toolbar, text="🗑️ Видалити", command=self.delete_publication).pack(side='left', padx=2)
        ttk.Button(toolbar, text="🔄 Оновити", command=self.load_data).pack(side='left', padx=2)
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('id', 'title', 'kind', 'authors', 'genres', 'type', 'year', 'location')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        self.tree.heading('id', text='ID')
        self.tree.heading('title', text='Назва')
        self.tree.heading('kind', text='Тип')
        self.tree.heading('authors', text='Автор(и)')
        self.tree.heading('genres', text='Жанр(и)')
        self.tree.heading('type', text='Вид')
        self.tree.heading('year', text='Рік')
        self.tree.heading('location', text='Місце')
        
        self.tree.column('id', width=40, anchor='center')
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
        
        # Double-click to edit
        self.tree.bind('<Double-1>', lambda e: self.edit_publication())
    
    def load_data(self):
        """Load publications from database."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        publications = models.get_all_publications()
        for pub in publications:
            kind_display = "📚 Книга" if pub.publication_kind == 'book' else "📰 Періодика"
            authors = ", ".join([a.name for a in pub.authors]) if pub.authors else "-"
            genres = ", ".join([g.name for g in pub.genres]) if pub.genres else "-"
            pub_type = pub.publication_type.name if pub.publication_type else "-"
            year = pub.year if pub.year else "-"
            location = str(pub.storage_location) if pub.storage_location else "-"
            
            self.tree.insert('', 'end', values=(
                pub.id, pub.title, kind_display, authors, genres, pub_type, year, location
            ))
    
    def get_selected_id(self):
        """Get the ID of selected item."""
        selection = self.tree.selection()
        if not selection:
            return None
        return self.tree.item(selection[0])['values'][0]
    
    def add_publication(self):
        """Show dialog to add new publication."""
        dialog = PublicationDialog(self, "Додати видання")
        self.wait_window(dialog)
        if dialog.result:
            try:
                models.create_publication(
                    title=dialog.result['title'],
                    publication_kind=dialog.result['kind'],
                    year=dialog.result['year'],
                    publication_type_id=dialog.result['type_id'],
                    storage_location_id=dialog.result['location_id'],
                    author_ids=dialog.result['author_ids'],
                    genre_ids=dialog.result['genre_ids']
                )
                self.load_data()
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося додати видання: {e}")
    
    def edit_publication(self):
        """Show dialog to edit selected publication."""
        pub_id = self.get_selected_id()
        if not pub_id:
            messagebox.showwarning("Увага", "Виберіть видання для редагування")
            return
        
        publication = models.get_publication_by_id(pub_id)
        if publication:
            dialog = PublicationDialog(self, "Редагувати видання", publication)
            self.wait_window(dialog)
            if dialog.result:
                try:
                    models.update_publication(
                        publication_id=pub_id,
                        title=dialog.result['title'],
                        publication_kind=dialog.result['kind'],
                        year=dialog.result['year'],
                        publication_type_id=dialog.result['type_id'],
                        storage_location_id=dialog.result['location_id'],
                        author_ids=dialog.result['author_ids'],
                        genre_ids=dialog.result['genre_ids']
                    )
                    self.load_data()
                except Exception as e:
                    messagebox.showerror("Помилка", f"Не вдалося оновити видання: {e}")
    
    def delete_publication(self):
        """Delete selected publication."""
        pub_id = self.get_selected_id()
        if not pub_id:
            messagebox.showwarning("Увага", "Виберіть видання для видалення")
            return
        
        if messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете видалити це видання?"):
            try:
                models.delete_publication(pub_id)
                self.load_data()
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося видалити видання: {e}")


class PublicationDialog(tk.Toplevel):
    """Dialog for adding/editing a publication."""
    
    def __init__(self, parent, title, publication=None):
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.publication = publication
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        
        self.geometry("500x550")
        self.minsize(400, 450)
        
        # Load reference data
        self.all_authors = models.get_all_authors()
        self.all_genres = models.get_all_genres()
        self.all_types = models.get_all_publication_types()
        self.all_locations = models.get_all_storage_locations()
        
        self.setup_ui()
        
        if publication:
            self.populate_form()
    
    def setup_ui(self):
        """Setup the UI components."""
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        ttk.Label(main_frame, text="Назва:").grid(row=0, column=0, sticky='w', pady=2)
        self.title_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.title_var, width=50).grid(row=0, column=1, sticky='ew', pady=2)
        
        # Publication kind (book/periodical)
        ttk.Label(main_frame, text="Тип:").grid(row=1, column=0, sticky='w', pady=2)
        self.kind_var = tk.StringVar(value='book')
        kind_frame = ttk.Frame(main_frame)
        kind_frame.grid(row=1, column=1, sticky='w', pady=2)
        ttk.Radiobutton(kind_frame, text="📚 Книга", variable=self.kind_var, value='book').pack(side='left')
        ttk.Radiobutton(kind_frame, text="📰 Періодичне видання", variable=self.kind_var, value='periodical').pack(side='left', padx=10)
        
        # Year
        ttk.Label(main_frame, text="Рік:").grid(row=2, column=0, sticky='w', pady=2)
        self.year_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.year_var, width=10).grid(row=2, column=1, sticky='w', pady=2)
        
        # Publication type
        ttk.Label(main_frame, text="Вид видання:").grid(row=3, column=0, sticky='w', pady=2)
        self.type_var = tk.StringVar()
        type_values = [""] + [t.name for t in self.all_types]
        self.type_combo = ttk.Combobox(main_frame, textvariable=self.type_var, values=type_values, state='readonly', width=30)
        self.type_combo.grid(row=3, column=1, sticky='w', pady=2)
        
        # Storage location
        ttk.Label(main_frame, text="Місце зберігання:").grid(row=4, column=0, sticky='w', pady=2)
        self.location_var = tk.StringVar()
        location_values = [""] + [str(loc) for loc in self.all_locations]
        self.location_combo = ttk.Combobox(main_frame, textvariable=self.location_var, values=location_values, state='readonly', width=30)
        self.location_combo.grid(row=4, column=1, sticky='w', pady=2)
        
        # Authors (multi-select listbox)
        ttk.Label(main_frame, text="Автори:").grid(row=5, column=0, sticky='nw', pady=2)
        authors_frame = ttk.Frame(main_frame)
        authors_frame.grid(row=5, column=1, sticky='ew', pady=2)
        
        self.authors_listbox = tk.Listbox(authors_frame, selectmode='multiple', height=5, exportselection=False)
        authors_scroll = ttk.Scrollbar(authors_frame, orient='vertical', command=self.authors_listbox.yview)
        self.authors_listbox.configure(yscrollcommand=authors_scroll.set)
        
        for author in self.all_authors:
            self.authors_listbox.insert('end', author.name)
        
        self.authors_listbox.pack(side='left', fill='both', expand=True)
        authors_scroll.pack(side='right', fill='y')
        
        # Genres (multi-select listbox)
        ttk.Label(main_frame, text="Жанри:").grid(row=6, column=0, sticky='nw', pady=2)
        genres_frame = ttk.Frame(main_frame)
        genres_frame.grid(row=6, column=1, sticky='ew', pady=2)
        
        self.genres_listbox = tk.Listbox(genres_frame, selectmode='multiple', height=5, exportselection=False)
        genres_scroll = ttk.Scrollbar(genres_frame, orient='vertical', command=self.genres_listbox.yview)
        self.genres_listbox.configure(yscrollcommand=genres_scroll.set)
        
        for genre in self.all_genres:
            self.genres_listbox.insert('end', genre.name)
        
        self.genres_listbox.pack(side='left', fill='both', expand=True)
        genres_scroll.pack(side='right', fill='y')
        
        # Hint
        hint = ttk.Label(main_frame, text="💡 Утримуйте Ctrl для вибору кількох авторів/жанрів", 
                        foreground='gray', font=('Helvetica', 9))
        hint.grid(row=7, column=0, columnspan=2, sticky='w', pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=(15, 0))
        
        ttk.Button(btn_frame, text="💾 Зберегти", command=self.save).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="❌ Скасувати", command=self.destroy).pack(side='left')
        
        # Configure grid weights
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Bind escape
        self.bind('<Escape>', lambda e: self.destroy())
    
    def populate_form(self):
        """Populate form with existing publication data."""
        pub = self.publication
        self.title_var.set(pub.title)
        self.kind_var.set(pub.publication_kind)
        self.year_var.set(str(pub.year) if pub.year else "")
        
        # Set publication type
        if pub.publication_type:
            self.type_var.set(pub.publication_type.name)
        
        # Set storage location
        if pub.storage_location:
            self.location_var.set(str(pub.storage_location))
        
        # Select authors
        author_names = [a.name for a in pub.authors]
        for i, author in enumerate(self.all_authors):
            if author.name in author_names:
                self.authors_listbox.selection_set(i)
        
        # Select genres
        genre_names = [g.name for g in pub.genres]
        for i, genre in enumerate(self.all_genres):
            if genre.name in genre_names:
                self.genres_listbox.selection_set(i)
    
    def save(self):
        """Validate and save the publication."""
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Увага", "Введіть назву видання")
            return
        
        kind = self.kind_var.get()
        
        # Parse year
        year_str = self.year_var.get().strip()
        year = None
        if year_str:
            try:
                year = int(year_str)
            except ValueError:
                messagebox.showwarning("Увага", "Некоректний рік")
                return
        
        # Get type ID
        type_id = None
        type_name = self.type_var.get()
        if type_name:
            for t in self.all_types:
                if t.name == type_name:
                    type_id = t.id
                    break
        
        # Get location ID
        location_id = None
        location_str = self.location_var.get()
        if location_str:
            for loc in self.all_locations:
                if str(loc) == location_str:
                    location_id = loc.id
                    break
        
        # Get selected authors
        author_ids = []
        for idx in self.authors_listbox.curselection():
            author_ids.append(self.all_authors[idx].id)
        
        # Get selected genres
        genre_ids = []
        for idx in self.genres_listbox.curselection():
            genre_ids.append(self.all_genres[idx].id)
        
        self.result = {
            'title': title,
            'kind': kind,
            'year': year,
            'type_id': type_id,
            'location_id': location_id,
            'author_ids': author_ids,
            'genre_ids': genre_ids
        }
        self.destroy()
