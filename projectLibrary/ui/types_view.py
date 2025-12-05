"""
Publication Types management view for Home Library application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import models


class TypesView(ttk.Frame):
    """Frame for managing publication types."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup the UI components."""
        # Title
        title_label = ttk.Label(self, text="Види видань", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(10, 5))
        
        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(toolbar, text="➕ Додати", command=self.add_type).pack(side='left', padx=2)
        ttk.Button(toolbar, text="✏️ Редагувати", command=self.edit_type).pack(side='left', padx=2)
        ttk.Button(toolbar, text="🗑️ Видалити", command=self.delete_type).pack(side='left', padx=2)
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, columns=('id', 'name'), show='headings', selectmode='browse')
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text="Назва виду")
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('name', width=300)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Double-click to edit
        self.tree.bind('<Double-1>', lambda e: self.edit_type())
    
    def load_data(self):
        """Load types from database."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        types = models.get_all_publication_types()
        for pub_type in types:
            self.tree.insert('', 'end', values=(pub_type.id, pub_type.name))
    
    def get_selected_id(self):
        """Get the ID of selected item."""
        selection = self.tree.selection()
        if not selection:
            return None
        return self.tree.item(selection[0])['values'][0]
    
    def add_type(self):
        """Show dialog to add new type."""
        dialog = TypeDialog(self, "Додати вид видання")
        self.wait_window(dialog)
        if dialog.result:
            try:
                models.create_publication_type(dialog.result)
                self.load_data()
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося додати вид: {e}")
    
    def edit_type(self):
        """Show dialog to edit selected type."""
        type_id = self.get_selected_id()
        if not type_id:
            messagebox.showwarning("Увага", "Виберіть вид для редагування")
            return
        
        pub_type = models.get_publication_type_by_id(type_id)
        if pub_type:
            dialog = TypeDialog(self, "Редагувати вид видання", pub_type.name)
            self.wait_window(dialog)
            if dialog.result:
                try:
                    models.update_publication_type(type_id, dialog.result)
                    self.load_data()
                except Exception as e:
                    messagebox.showerror("Помилка", f"Не вдалося оновити вид: {e}")
    
    def delete_type(self):
        """Delete selected type."""
        type_id = self.get_selected_id()
        if not type_id:
            messagebox.showwarning("Увага", "Виберіть вид для видалення")
            return
        
        if messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете видалити цей вид?"):
            try:
                models.delete_publication_type(type_id)
                self.load_data()
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося видалити вид: {e}")


class TypeDialog(tk.Toplevel):
    """Dialog for adding/editing a publication type."""
    
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
        
        ttk.Label(frame, text="Назва виду:").pack(anchor='w')
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
            messagebox.showwarning("Увага", "Введіть назву виду")
