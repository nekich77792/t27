"""
Main window for Home Library application.
"""
import tkinter as tk
from tkinter import ttk
from ui.publications_view import PublicationsView
from ui.authors_view import AuthorsView
from ui.genres_view import GenresView
from ui.types_view import TypesView
from ui.locations_view import LocationsView
from ui.search_view import SearchView


class MainWindow:
    """Main application window with tabbed interface."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Домашня Бібліотека")
        self.root.geometry("1000x650")
        self.root.minsize(800, 500)
        
        # Configure style
        self.setup_style()
        
        # Create main layout
        self.setup_ui()
    
    def setup_style(self):
        """Configure ttk styles for better appearance."""
        style = ttk.Style()
        
        # Try to use a modern theme
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'vista' in available_themes:
            style.theme_use('vista')
        
        # Configure Treeview
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Configure Notebook tabs
        style.configure("TNotebook.Tab", padding=[15, 5], font=('Helvetica', 10))
    
    def setup_ui(self):
        """Setup the main UI."""
        # Header
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill='x')
        
        title_label = ttk.Label(
            header_frame, 
            text="📚 Домашня Бібліотека", 
            font=('Helvetica', 20, 'bold')
        )
        title_label.pack()
        
        subtitle = ttk.Label(
            header_frame,
            text="Система управління книгами та періодичними виданнями",
            font=('Helvetica', 10),
            foreground='gray'
        )
        subtitle.pack()
        
        # Separator
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', pady=5)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Create tabs
        self.publications_view = PublicationsView(self.notebook)
        self.notebook.add(self.publications_view, text="📖 Видання")
        
        self.authors_view = AuthorsView(self.notebook)
        self.notebook.add(self.authors_view, text="✍️ Автори")
        
        self.genres_view = GenresView(self.notebook)
        self.notebook.add(self.genres_view, text="🏷️ Жанри")
        
        self.types_view = TypesView(self.notebook)
        self.notebook.add(self.types_view, text="📋 Види")
        
        self.locations_view = LocationsView(self.notebook)
        self.notebook.add(self.locations_view, text="📍 Місця")
        
        self.search_view = SearchView(self.notebook)
        self.notebook.add(self.search_view, text="🔍 Пошук")
        
        # Bind tab change to refresh data
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        
        # Status bar
        self.status_var = tk.StringVar(value="Готово")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief='sunken', anchor='w')
        status_bar.pack(fill='x', side='bottom')
    
    def on_tab_changed(self, event):
        """Handle tab change event - refresh data in the selected tab."""
        selected_tab = self.notebook.select()
        tab_name = self.notebook.tab(selected_tab, 'text')
        
        # Refresh data in the current tab
        if "Видання" in tab_name:
            self.publications_view.load_data()
        elif "Автори" in tab_name:
            self.authors_view.load_data()
        elif "Жанри" in tab_name:
            self.genres_view.load_data()
        elif "Види" in tab_name:
            self.types_view.load_data()
        elif "Місця" in tab_name:
            self.locations_view.load_data()
        elif "Пошук" in tab_name:
            self.search_view.refresh_dropdowns()


def create_main_window():
    """Create and return the main window."""
    root = tk.Tk()
    app = MainWindow(root)
    return root
