"""
Storage Locations management view for Home Library application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import models


class LocationsView(ttk.Frame):
    """Frame for managing storage locations."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup the UI components."""
        # Title
        title_label = ttk.Label(self, text="Місця зберігання", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(10, 5))
        
        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(toolbar, text="➕ Додати", command=self.add_location).pack(side='left', padx=2)
        ttk.Button(toolbar, text="✏️ Редагувати", command=self.edit_location).pack(side='left', padx=2)
        ttk.Button(toolbar, text="🗑️ Видалити", command=self.delete_location).pack(side='left', padx=2)
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, columns=('id', 'cabinet', 'shelf'), show='headings', selectmode='browse')
        self.tree.heading('id', text='ID')
        self.tree.heading('cabinet', text="Шафа")
        self.tree.heading('shelf', text="Полиця")
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('cabinet', width=150)
        self.tree.column('shelf', width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Double-click to edit
        self.tree.bind('<Double-1>', lambda e: self.edit_location())
    
    def load_data(self):
        """Load locations from database."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        locations = models.get_all_storage_locations()
        for loc in locations:
            self.tree.insert('', 'end', values=(loc.id, loc.cabinet, loc.shelf))
    
    def get_selected_id(self):
        """Get the ID of selected item."""
        selection = self.tree.selection()
        if not selection:
            return None
        return self.tree.item(selection[0])['values'][0]
    
    def add_location(self):
        """Show dialog to add new location."""
        dialog = LocationDialog(self, "Додати місце зберігання")
        self.wait_window(dialog)
        if dialog.result:
            try:
                models.create_storage_location(dialog.result[0], dialog.result[1])
                self.load_data()
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося додати місце: {e}")
    
    def edit_location(self):
        """Show dialog to edit selected location."""
        location_id = self.get_selected_id()
        if not location_id:
            messagebox.showwarning("Увага", "Виберіть місце для редагування")
            return
        
        location = models.get_storage_location_by_id(location_id)
        if location:
            dialog = LocationDialog(self, "Редагувати місце зберігання", 
                                    location.cabinet, location.shelf)
            self.wait_window(dialog)
            if dialog.result:
                try:
                    models.update_storage_location(location_id, dialog.result[0], dialog.result[1])
                    self.load_data()
                except Exception as e:
                    messagebox.showerror("Помилка", f"Не вдалося оновити місце: {e}")
    
    def delete_location(self):
        """Delete selected location."""
        location_id = self.get_selected_id()
        if not location_id:
            messagebox.showwarning("Увага", "Виберіть місце для видалення")
            return
        
        if messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете видалити це місце?"):
            try:
                models.delete_storage_location(location_id)
                self.load_data()
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося видалити місце: {e}")


class LocationDialog(tk.Toplevel):
    """Dialog for adding/editing a storage location."""
    
    def __init__(self, parent, title, cabinet="", shelf=""):
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center the dialog
        self.geometry("300x160")
        
        # Form
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Шафа:").pack(anchor='w')
        self.cabinet_var = tk.StringVar(value=cabinet)
        self.cabinet_entry = ttk.Entry(frame, textvariable=self.cabinet_var, width=40)
        self.cabinet_entry.pack(fill='x', pady=(0, 5))
        self.cabinet_entry.focus_set()
        
        ttk.Label(frame, text="Полиця:").pack(anchor='w')
        self.shelf_var = tk.StringVar(value=shelf)
        self.shelf_entry = ttk.Entry(frame, textvariable=self.shelf_var, width=40)
        self.shelf_entry.pack(fill='x', pady=(0, 5))
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(btn_frame, text="Зберегти", command=self.save).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Скасувати", command=self.destroy).pack(side='left')
        
        # Bind Enter key
        self.shelf_entry.bind('<Return>', lambda e: self.save())
        self.bind('<Escape>', lambda e: self.destroy())
    
    def save(self):
        """Save and close dialog."""
        cabinet = self.cabinet_var.get().strip()
        shelf = self.shelf_var.get().strip()
        if cabinet and shelf:
            self.result = (cabinet, shelf)
            self.destroy()
        else:
            messagebox.showwarning("Увага", "Заповніть всі поля")
