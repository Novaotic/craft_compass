"""Main application window."""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from database.database import CraftCompassDB
from controllers.item_controllers import ItemController
from controllers.project_controller import ProjectController
from controllers.report_controller import ReportController
from controllers.tag_controller import TagController
from controllers.export_controller import ExportController
from ui.item_form import ItemForm
from ui.project_form import ProjectForm
from ui.report_view import ReportView
from ui.search_filter_widget import SearchFilterWidget
from ui.tag_manager import TagManager
from ui.export_dialog import ExportDialog
from ui.import_dialog import ImportDialog
from utils.helpers import format_date_display, format_quantity


def format_tags_display(tags):
    """
    Format tags for display with color indicators.
    
    Args:
        tags: List of Tag objects
    
    Returns:
        Formatted string with tag names
    """
    if not tags:
        return ""
    
    # Just return tag names - colors will be applied via tkinter tags
    return ", ".join([tag.name for tag in tags])


def get_tag_color_for_styling(tags):
    """
    Get the primary tag color for row styling.
    
    Args:
        tags: List of Tag objects
    
    Returns:
        Tuple of (tkinter_tag_name, color_name) or (None, None)
    """
    if not tags:
        return None, None
    
    # Use the first tag's color for row styling
    first_tag = tags[0]
    tag_color = getattr(first_tag, 'color', None) if hasattr(first_tag, 'color') else None
    
    if tag_color and str(tag_color).strip():
        color_lower = str(tag_color).strip().lower()
        # Check if it's a named color we support
        supported_colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'gray', 'grey']
        if color_lower in supported_colors:
            return f"tag_{color_lower}", color_lower
        # Check if it's a hex color
        elif color_lower.startswith('#'):
            return "tag_hex", color_lower
    
    return None, None


class MainWindow:
    def __init__(self, db: CraftCompassDB):
        """
        Initialize the main application window.
        
        Args:
            db: CraftCompassDB instance
        """
        self.db = db
        self.item_controller = ItemController(db)
        self.project_controller = ProjectController(db)
        self.report_controller = ReportController(db)
        self.tag_controller = TagController(db)
        self.export_controller = ExportController(db)
        
        # Search/filter state
        self.items_search_term = ""
        self.items_filters = {}
        self.projects_search_term = ""
        self.projects_filters = {}
        self.suppliers_search_term = ""
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Craft Compass")
        self.root.geometry("900x600")
        
        self._create_menu()
        self._create_widgets()
        self._refresh_all()
    
    def _create_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export...", command=self._export_data, accelerator="Ctrl+E")
        file_menu.add_command(label="Import...", command=self._import_data, accelerator="Ctrl+I")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Manage Tags...", command=self._manage_tags)
        
        # Keyboard shortcuts
        self.root.bind('<Control-e>', lambda e: self._export_data())
        self.root.bind('<Control-i>', lambda e: self._import_data())
    
    def _create_widgets(self):
        """Create the main window widgets."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Items tab
        self.items_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.items_frame, text="Items")
        self._create_items_tab()
        
        # Projects tab
        self.projects_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.projects_frame, text="Projects")
        self._create_projects_tab()
        
        # Suppliers tab
        self.suppliers_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.suppliers_frame, text="Suppliers")
        self._create_suppliers_tab()
        
        # Reports tab
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_frame, text="Reports")
        self._create_reports_tab()
    
    def _create_items_tab(self):
        """Create the items tab."""
        # Toolbar
        toolbar = ttk.Frame(self.items_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(toolbar, text="New Item", command=self._new_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Edit Item", command=self._edit_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete Item", command=self._delete_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Refresh", command=self._refresh_items).pack(side=tk.LEFT, padx=2)
        
        # Search and filter
        categories = list(set([item.category for item in self.item_controller.get_all_items() if item.category]))
        suppliers = self.db.suppliers.get_all_suppliers()
        supplier_names = [s['name'] for s in suppliers]
        
        filter_options = {
            'Category': categories,
            'Supplier': supplier_names
        }
        
        self.items_search_filter = SearchFilterWidget(
            self.items_frame,
            on_search=self._on_items_search,
            on_filter=self._on_items_filter,
            filter_options=filter_options
        )
        self.items_search_filter.pack(fill=tk.X, padx=5, pady=5)
        
        # Items list
        list_frame = ttk.Frame(self.items_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview with scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.items_tree = ttk.Treeview(list_frame, columns=("Category", "Quantity", "Unit", "Supplier", "Date", "Tags"), 
                                       show="headings", yscrollcommand=scrollbar.set)
        self.items_tree.heading("#0", text="ID")
        self.items_tree.heading("Category", text="Category")
        self.items_tree.heading("Quantity", text="Quantity")
        self.items_tree.heading("Unit", text="Unit")
        self.items_tree.heading("Supplier", text="Supplier")
        self.items_tree.heading("Date", text="Purchase Date")
        self.items_tree.heading("Tags", text="Tags")
        
        self.items_tree.column("#0", width=50)
        self.items_tree.column("Category", width=120)
        self.items_tree.column("Quantity", width=80)
        self.items_tree.column("Unit", width=80)
        self.items_tree.column("Supplier", width=120)
        self.items_tree.column("Date", width=100)
        self.items_tree.column("Tags", width=150)
        
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.items_tree.yview)
        
        # Configure tag colors for row styling (tkinter tags, not our tags)
        self._configure_tag_colors()
    
    def _create_projects_tab(self):
        """Create the projects tab."""
        # Toolbar
        toolbar = ttk.Frame(self.projects_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(toolbar, text="New Project", command=self._new_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Edit Project", command=self._edit_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete Project", command=self._delete_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Refresh", command=self._refresh_projects).pack(side=tk.LEFT, padx=2)
        
        # Search and filter
        self.projects_search_filter = SearchFilterWidget(
            self.projects_frame,
            on_search=self._on_projects_search,
            on_filter=self._on_projects_filter
        )
        self.projects_search_filter.pack(fill=tk.X, padx=5, pady=5)
        
        # Projects list
        list_frame = ttk.Frame(self.projects_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview with scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.projects_tree = ttk.Treeview(list_frame, columns=("Description", "Date Created", "Materials", "Tags"), 
                                          show="headings", yscrollcommand=scrollbar.set)
        self.projects_tree.heading("#0", text="ID")
        self.projects_tree.heading("Description", text="Description")
        self.projects_tree.heading("Date Created", text="Date Created")
        self.projects_tree.heading("Materials", text="Materials Count")
        self.projects_tree.heading("Tags", text="Tags")
        
        self.projects_tree.column("#0", width=50)
        self.projects_tree.column("Description", width=250)
        self.projects_tree.column("Date Created", width=120)
        self.projects_tree.column("Materials", width=100)
        self.projects_tree.column("Tags", width=150)
        
        self.projects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.projects_tree.yview)
        
        # Configure tag colors for projects tree
        self._configure_tag_colors()
    
    def _create_suppliers_tab(self):
        """Create the suppliers tab."""
        # Toolbar
        toolbar = ttk.Frame(self.suppliers_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(toolbar, text="New Supplier", command=self._new_supplier).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Edit Supplier", command=self._edit_supplier).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete Supplier", command=self._delete_supplier).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Refresh", command=self._refresh_suppliers).pack(side=tk.LEFT, padx=2)
        
        # Search
        search_frame = ttk.Frame(self.suppliers_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.suppliers_search_var = tk.StringVar()
        self.suppliers_search_var.trace_add('write', self._on_suppliers_search)
        ttk.Entry(search_frame, textvariable=self.suppliers_search_var, width=40).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(search_frame, text="Clear", command=lambda: self.suppliers_search_var.set("")).pack(side=tk.LEFT, padx=5)
        
        # Suppliers list
        list_frame = ttk.Frame(self.suppliers_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview with scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.suppliers_tree = ttk.Treeview(list_frame, columns=("Contact", "Website", "Notes"), 
                                            show="headings", yscrollcommand=scrollbar.set)
        self.suppliers_tree.heading("#0", text="ID")
        self.suppliers_tree.heading("Contact", text="Contact Info")
        self.suppliers_tree.heading("Website", text="Website")
        self.suppliers_tree.heading("Notes", text="Notes")
        
        self.suppliers_tree.column("#0", width=50)
        self.suppliers_tree.column("Contact", width=200)
        self.suppliers_tree.column("Website", width=200)
        self.suppliers_tree.column("Notes", width=300)
        
        self.suppliers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.suppliers_tree.yview)
    
    def _configure_tag_colors(self):
        """Configure tkinter tag colors for row styling based on tag colors."""
        # Color mapping for common color names to tkinter colors
        color_map = {
            'red': '#ffcccc',
            'blue': '#ccccff',
            'green': '#ccffcc',
            'yellow': '#ffffcc',
            'orange': '#ffe6cc',
            'purple': '#e6ccff',
            'pink': '#ffccff',
            'gray': '#e0e0e0',
            'grey': '#e0e0e0',
        }
        
        # Configure tkinter tags for each color
        for color_name, bg_color in color_map.items():
            if hasattr(self, 'items_tree'):
                self.items_tree.tag_configure(f"tag_{color_name}", background=bg_color)
            if hasattr(self, 'projects_tree'):
                self.projects_tree.tag_configure(f"tag_{color_name}", background=bg_color)
        
        # Default tag for hex colors
        if hasattr(self, 'items_tree'):
            self.items_tree.tag_configure("tag_hex", background='#f0f0f0')
        if hasattr(self, 'projects_tree'):
            self.projects_tree.tag_configure("tag_hex", background='#f0f0f0')
    
    def _create_reports_tab(self):
        """Create the reports tab."""
        self.report_view = ReportView(self.reports_frame, self.report_controller)
        self.report_view.pack(fill=tk.BOTH, expand=True)
    
    def _on_items_search(self, search_term: str):
        """Handle items search."""
        self.items_search_term = search_term
        self._refresh_items()
    
    def _on_items_filter(self, filters: dict):
        """Handle items filter."""
        self.items_filters = filters
        self._refresh_items()
    
    def _refresh_items(self):
        """Refresh the items list."""
        # Clear existing items
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        # Apply search and filter
        if self.items_search_term:
            items = self.item_controller.search_items(self.items_search_term)
        elif self.items_filters:
            category = self.items_filters.get('Category')
            supplier_name = self.items_filters.get('Supplier')
            supplier_id = None
            if supplier_name:
                suppliers = self.db.suppliers.get_all_suppliers()
                supplier = next((s for s in suppliers if s['name'] == supplier_name), None)
                supplier_id = supplier['id'] if supplier else None
            items = self.item_controller.filter_items(category=category, supplier_id=supplier_id)
        else:
            items = self.item_controller.get_all_items()
        
        suppliers = self.db.suppliers.get_all_suppliers()
        supplier_dict = {s['id']: s['name'] for s in suppliers}
        
        for item in items:
            supplier_name = supplier_dict.get(item.supplier_id, "") if item.supplier_id else ""
            date_str = format_date_display(item.purchase_date) if item.purchase_date else ""
            
            # Get tags for this item
            item_tags = self.tag_controller.get_item_tags(item.id)
            tag_names = format_tags_display(item_tags)
            
            # Get color tag for row styling
            tk_tag, _ = get_tag_color_for_styling(item_tags)
            tags_list = [tk_tag] if tk_tag else []
            
            item_id = self.items_tree.insert("", tk.END, text=str(item.id), 
                                  values=(item.category or "", 
                                         str(item.quantity) if item.quantity else "",
                                         item.unit or "",
                                         supplier_name,
                                         date_str,
                                         tag_names),
                                  tags=tags_list)
    
    def _on_projects_search(self, search_term: str):
        """Handle projects search."""
        self.projects_search_term = search_term
        self._refresh_projects()
    
    def _on_projects_filter(self, filters: dict):
        """Handle projects filter."""
        self.projects_filters = filters
        self._refresh_projects()
    
    def _refresh_projects(self):
        """Refresh the projects list."""
        # Clear existing projects
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
        
        # Apply search and filter
        if self.projects_search_term:
            projects = self.project_controller.search_projects(self.projects_search_term)
        elif self.projects_filters:
            # For now, just use search - can enhance filters later
            projects = self.project_controller.get_all_projects()
        else:
            projects = self.project_controller.get_all_projects()
        
        for project in projects:
            date_str = format_date_display(project.date_created) if project.date_created else ""
            materials_count = len(project.materials_used)
            
            # Get tags for this project
            project_tags = self.tag_controller.get_project_tags(project.id)
            tag_names = format_tags_display(project_tags)
            
            # Get color tag for row styling
            tk_tag, _ = get_tag_color_for_styling(project_tags)
            tags_list = [tk_tag] if tk_tag else []
            
            self.projects_tree.insert("", tk.END, text=str(project.id),
                                     values=(project.description or "",
                                            date_str,
                                            str(materials_count),
                                            tag_names),
                                     tags=tags_list)
    
    def _on_suppliers_search(self, *args):
        """Handle suppliers search."""
        self.suppliers_search_term = self.suppliers_search_var.get().strip()
        self._refresh_suppliers()
    
    def _refresh_suppliers(self):
        """Refresh the suppliers list."""
        # Clear existing suppliers
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
        
        # Apply search
        if self.suppliers_search_term:
            suppliers = self.db.suppliers.search_suppliers(self.suppliers_search_term)
        else:
            suppliers = self.db.suppliers.get_all_suppliers()
        
        for supplier in suppliers:
            self.suppliers_tree.insert("", tk.END, text=str(supplier['id']),
                                      values=(supplier['contact_info'],
                                             supplier['website'] or "",
                                             supplier['notes'] or ""))
    
    def _refresh_all(self):
        """Refresh all tabs."""
        self._refresh_items()
        self._refresh_projects()
        self._refresh_suppliers()
        if hasattr(self, 'report_view'):
            self.report_view.refresh()
    
    def _new_item(self):
        """Open form to create a new item."""
        suppliers = self.db.suppliers.get_all_suppliers()
        form = ItemForm(self.root, self.db, suppliers, on_save=self._save_item)
        self.root.wait_window(form.dialog)
        if form.result:
            self._refresh_items()
    
    def _edit_item(self):
        """Open form to edit selected item."""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to edit")
            return
        
        item_id = int(self.items_tree.item(selection[0])['text'])
        item = self.item_controller.get_item(item_id)
        if not item:
            messagebox.showerror("Error", "Item not found")
            return
        
        suppliers = self.db.suppliers.get_all_suppliers()
        form = ItemForm(self.root, self.db, suppliers, on_save=self._update_item, item_data=item.to_dict())
        self.root.wait_window(form.dialog)
        if form.result:
            self._refresh_items()
    
    def _delete_item(self):
        """Delete selected item."""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
            return
        
        item_id = int(self.items_tree.item(selection[0])['text'])
        try:
            self.item_controller.delete_item(item_id)
            messagebox.showinfo("Success", "Item deleted successfully")
            self._refresh_items()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete item: {str(e)}")
    
    def _save_item(self, item_data):
        """Save a new item."""
        try:
            tag_ids = item_data.pop('tag_ids', [])
            item_id = self.item_controller.create_item(**item_data)
            # Add tags
            for tag_id in tag_ids:
                self.tag_controller.add_tag_to_item(item_id, tag_id)
            messagebox.showinfo("Success", "Item created successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create item: {str(e)}")
    
    def _update_item(self, item_data):
        """Update an existing item."""
        selection = self.items_tree.selection()
        if not selection:
            return
        
        item_id = int(self.items_tree.item(selection[0])['text'])
        try:
            tag_ids = item_data.pop('tag_ids', [])
            self.item_controller.update_item(item_id, **item_data)
            # Update tags - remove all and re-add
            existing_tags = self.tag_controller.get_item_tags(item_id)
            for tag in existing_tags:
                self.tag_controller.remove_tag_from_item(item_id, tag.id)
            for tag_id in tag_ids:
                self.tag_controller.add_tag_to_item(item_id, tag_id)
            messagebox.showinfo("Success", "Item updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update item: {str(e)}")
    
    def _new_project(self):
        """Open form to create a new project."""
        items = self.item_controller.get_all_items()
        items_list = [{'id': item.id, 'name': item.name} for item in items]
        form = ProjectForm(self.root, self.db, items_list, on_save=self._save_project)
        self.root.wait_window(form.dialog)
        if form.result:
            self._refresh_projects()
    
    def _edit_project(self):
        """Open form to edit selected project."""
        selection = self.projects_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a project to edit")
            return
        
        project_id = int(self.projects_tree.item(selection[0])['text'])
        project = self.project_controller.get_project(project_id)
        if not project:
            messagebox.showerror("Error", "Project not found")
            return
        
        items = self.item_controller.get_all_items()
        items_list = [{'id': item.id, 'name': item.name} for item in items]
        project_dict = project.to_dict()
        form = ProjectForm(self.root, self.db, items_list, on_save=self._update_project, project_data=project_dict)
        self.root.wait_window(form.dialog)
        if form.result:
            self._refresh_projects()
    
    def _delete_project(self):
        """Delete selected project."""
        selection = self.projects_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a project to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this project?"):
            return
        
        project_id = int(self.projects_tree.item(selection[0])['text'])
        try:
            self.project_controller.delete_project(project_id)
            messagebox.showinfo("Success", "Project deleted successfully")
            self._refresh_projects()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete project: {str(e)}")
    
    def _save_project(self, project_data):
        """Save a new project."""
        try:
            tag_ids = project_data.pop('tag_ids', [])
            project_id = self.project_controller.create_project(
                name=project_data['name'],
                description=project_data['description'],
                date_created=project_data['date_created']
            )
            # Add materials
            for item_id, quantity in project_data['materials_used']:
                self.project_controller.add_material_to_project(project_id, item_id, quantity)
            # Add tags
            for tag_id in tag_ids:
                self.tag_controller.add_tag_to_project(project_id, tag_id)
            messagebox.showinfo("Success", "Project created successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create project: {str(e)}")
    
    def _update_project(self, project_data):
        """Update an existing project."""
        selection = self.projects_tree.selection()
        if not selection:
            return
        
        project_id = int(self.projects_tree.item(selection[0])['text'])
        try:
            tag_ids = project_data.pop('tag_ids', [])
            # Update project
            self.project_controller.update_project(
                project_id=project_id,
                name=project_data['name'],
                description=project_data['description'],
                date_created=project_data['date_created']
            )
            # Update materials - remove all and re-add
            existing_materials = self.project_controller.get_project_materials(project_id)
            for mat in existing_materials:
                self.project_controller.remove_material_from_project(mat['id'])
            # Add new materials
            for item_id, quantity in project_data['materials_used']:
                self.project_controller.add_material_to_project(project_id, item_id, quantity)
            # Update tags - remove all and re-add
            existing_tags = self.tag_controller.get_project_tags(project_id)
            for tag in existing_tags:
                self.tag_controller.remove_tag_from_project(project_id, tag.id)
            for tag_id in tag_ids:
                self.tag_controller.add_tag_to_project(project_id, tag_id)
            messagebox.showinfo("Success", "Project updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update project: {str(e)}")
    
    def _new_supplier(self):
        """Open simple dialog to create a new supplier."""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Supplier")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.minsize(500, 280)
        dialog.geometry("500x280")
        
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(frame, text="Name *:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=name_var, width=40).grid(row=0, column=1, pady=5, padx=5, sticky=tk.W+tk.E)
        
        ttk.Label(frame, text="Contact Info *:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        contact_var = tk.StringVar()
        ttk.Entry(frame, textvariable=contact_var, width=40).grid(row=1, column=1, pady=5, padx=5, sticky=tk.W+tk.E)
        
        ttk.Label(frame, text="Website:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        website_var = tk.StringVar()
        ttk.Entry(frame, textvariable=website_var, width=40).grid(row=2, column=1, pady=5, padx=5, sticky=tk.W+tk.E)
        
        ttk.Label(frame, text="Notes:").grid(row=3, column=0, sticky=tk.W+tk.N, pady=5, padx=5)
        notes_text = tk.Text(frame, width=40, height=4, wrap=tk.WORD)
        notes_text.grid(row=3, column=1, pady=5, padx=5, sticky=tk.W+tk.E)
        
        def save():
            if not name_var.get().strip() or not contact_var.get().strip():
                messagebox.showerror("Error", "Name and Contact Info are required")
                return
            try:
                self.db.suppliers.add_supplier(
                    name=name_var.get().strip(),
                    contact_info=contact_var.get().strip(),
                    website=website_var.get().strip() or None,
                    notes=notes_text.get('1.0', tk.END).strip() or None
                )
                messagebox.showinfo("Success", "Supplier created successfully")
                dialog.destroy()
                self._refresh_suppliers()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create supplier: {str(e)}")
        
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)
        ttk.Button(button_frame, text="Save", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_reqwidth()
        height = dialog.winfo_reqheight()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def _edit_supplier(self):
        """Edit selected supplier (simplified - can be enhanced later)."""
        selection = self.suppliers_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a supplier to edit")
            return
        messagebox.showinfo("Info", "Supplier editing will be enhanced in a future update")
    
    def _delete_supplier(self):
        """Delete selected supplier."""
        selection = self.suppliers_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a supplier to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this supplier?"):
            return
        
        supplier_id = int(self.suppliers_tree.item(selection[0])['text'])
        try:
            self.db.suppliers.delete_supplier(supplier_id)
            messagebox.showinfo("Success", "Supplier deleted successfully")
            self._refresh_suppliers()
            self._refresh_items()  # Refresh items in case supplier was referenced
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete supplier: {str(e)}")
    
    def _manage_tags(self):
        """Open tag management dialog."""
        tag_manager = TagManager(self.root, self.tag_controller, on_update=self._refresh_all)
        self.root.wait_window(tag_manager.dialog)
    
    def _export_data(self):
        """Open export dialog."""
        export_dialog = ExportDialog(self.root, self.export_controller)
        self.root.wait_window(export_dialog.dialog)
        # Refresh after export in case data changed
        self._refresh_all()
    
    def _import_data(self):
        """Open import dialog."""
        import_dialog = ImportDialog(self.root, self.export_controller)
        self.root.wait_window(import_dialog.dialog)
        # Refresh after import
        self._refresh_all()
    
    def run(self):
        """Start the main event loop."""
        self.root.mainloop()

