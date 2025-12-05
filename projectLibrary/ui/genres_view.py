"""
Genres management view for Home Library application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import models


class GenresView(ttk.Frame):
    """Frame for managing genres."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup the UI components."""
        # Title
        title_label = ttk.Label(self, text="Жанри", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(10, 5))
        
        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(toolbar, text="➕ Додати", command=self.add_genre).pack(side='left', padx=2)
        ttk.Button(toolbar, text="✏️ Редагувати", command=self.edit_genre).pack(side='left', padx=2)
        ttk.Button(toolbar, text="🗑️ Видалити", command=self.delete_genre).pack(side='left', padx=2)
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, columns=('id', 'name'), show='headings', selectmode='browse')
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text="Назва жанру")
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('name', width=300)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Double-click to edit
        self.tree.bind('<Double-1>', lambda e: self.edit_genre())
    
    def load_data(self):
        """Load genres from database."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        genres = models.get_all_genres()
        for genre in genres:
            self.tree.insert('', 'end', values=(genre.id, genre.name))
    
    def get_selected_id(self):
        """Get the ID of selected item."""
        selection = self.tree.selection()
        if not selection:
            return None
        return self.tree.item(selection[0])['values'][0]
    
    def add_genre(self):
        """Show dialog to add new genre."""
        dialog = GenreDialog(self, "Додати жанр")
        self.wait_window(dialog)
        if dialog.result:
            try:
                models.create_genre(dialog.result)
                self.load_data()
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося додати жанр: {e}")
    
    def edit_genre(self):
        """Show dialog to edit selected genre."""
        genre_id = self.get_selected_id()
        if not genre_id:
            messagebox.showwarning("Увага", "Виберіть жанр для редагування")
            return
        
        genre = models.get_genre_by_id(genre_id)
        if genre:
            dialog = GenreDialog(self, "Редагувати жанр", genre.name)
            self.wait_window(dialog)
            if dialog.result:
                try:
                    models.update_genre(genre_id, dialog.result)
                    self.load_data()
                except Exception as e:
                    messagebox.showerror("Помилка", f"Не вдалося оновити жанр: {e}")
    
    def delete_genre(self):
        """Delete selected genre."""
        genre_id = self.get_selected_id()
        if not genre_id:
            messagebox.showwarning("Увага", "Виберіть жанр для видалення")
            return
        
        if messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете видалити цей жанр?"):
            try:
                models.delete_genre(genre_id)
                self.load_data()
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося видалити жанр: {e}")


class GenreDialog(tk.Toplevel):
    """Dialog for adding/editing a genre."""
    
    def __init__(self, parent, title, initial_value=""):
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center the dialog
        self.geometry("300x120")
        
        # Form
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Назва жанру:").pack(anchor='w')
        self.name_var = tk.StringVar(value=initial_value)
        self.name_entry = ttk.Entry(frame, textvariable=self.name_var, width=40)
        self.name_entry.pack(fill='x', pady=5)
        self.name_entry.focus_set()
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(btn_frame, text="Зберегти", command=self.save).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Скасувати", command=self.destroy).pack(side='left')
        
        # Bind Enter key
        self.name_entry.bind('<Return>', lambda e: self.save())
        self.bind('<Escape>', lambda e: self.destroy())
    
    def save(self):
        """Save and close dialog."""
        name = self.name_var.get().strip()
        if name:
            self.result = name
            self.destroy()
        else:
            messagebox.showwarning("Увага", "Введіть назву жанру")
