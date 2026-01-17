"""Main application window."""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from database.database import CraftCompassDB
from controllers.item_controllers import ItemController
from controllers.project_controller import ProjectController
from controllers.report_controller import ReportController
from ui.item_form import ItemForm
from ui.project_form import ProjectForm
from ui.report_view import ReportView
from utils.helpers import format_date_display, format_quantity


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
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Craft Compass")
        self.root.geometry("900x600")
        
        self._create_widgets()
        self._refresh_all()
    
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
        
        # Items list
        list_frame = ttk.Frame(self.items_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview with scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.items_tree = ttk.Treeview(list_frame, columns=("Category", "Quantity", "Unit", "Supplier", "Date"), 
                                       show="headings", yscrollcommand=scrollbar.set)
        self.items_tree.heading("#0", text="ID")
        self.items_tree.heading("Category", text="Category")
        self.items_tree.heading("Quantity", text="Quantity")
        self.items_tree.heading("Unit", text="Unit")
        self.items_tree.heading("Supplier", text="Supplier")
        self.items_tree.heading("Date", text="Purchase Date")
        
        self.items_tree.column("#0", width=50)
        self.items_tree.column("Category", width=150)
        self.items_tree.column("Quantity", width=100)
        self.items_tree.column("Unit", width=100)
        self.items_tree.column("Supplier", width=150)
        self.items_tree.column("Date", width=120)
        
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.items_tree.yview)
    
    def _create_projects_tab(self):
        """Create the projects tab."""
        # Toolbar
        toolbar = ttk.Frame(self.projects_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(toolbar, text="New Project", command=self._new_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Edit Project", command=self._edit_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete Project", command=self._delete_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Refresh", command=self._refresh_projects).pack(side=tk.LEFT, padx=2)
        
        # Projects list
        list_frame = ttk.Frame(self.projects_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview with scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.projects_tree = ttk.Treeview(list_frame, columns=("Description", "Date Created", "Materials"), 
                                          show="headings", yscrollcommand=scrollbar.set)
        self.projects_tree.heading("#0", text="ID")
        self.projects_tree.heading("Description", text="Description")
        self.projects_tree.heading("Date Created", text="Date Created")
        self.projects_tree.heading("Materials", text="Materials Count")
        
        self.projects_tree.column("#0", width=50)
        self.projects_tree.column("Description", width=300)
        self.projects_tree.column("Date Created", width=120)
        self.projects_tree.column("Materials", width=120)
        
        self.projects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.projects_tree.yview)
    
    def _create_suppliers_tab(self):
        """Create the suppliers tab."""
        # Toolbar
        toolbar = ttk.Frame(self.suppliers_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(toolbar, text="New Supplier", command=self._new_supplier).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Edit Supplier", command=self._edit_supplier).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete Supplier", command=self._delete_supplier).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Refresh", command=self._refresh_suppliers).pack(side=tk.LEFT, padx=2)
        
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
    
    def _create_reports_tab(self):
        """Create the reports tab."""
        self.report_view = ReportView(self.reports_frame, self.report_controller)
        self.report_view.pack(fill=tk.BOTH, expand=True)
    
    def _refresh_items(self):
        """Refresh the items list."""
        # Clear existing items
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        # Load items
        items = self.item_controller.get_all_items()
        suppliers = self.db.suppliers.get_all_suppliers()
        supplier_dict = {s['id']: s['name'] for s in suppliers}
        
        for item in items:
            supplier_name = supplier_dict.get(item.supplier_id, "") if item.supplier_id else ""
            date_str = format_date_display(item.purchase_date) if item.purchase_date else ""
            
            self.items_tree.insert("", tk.END, text=str(item.id), 
                                  values=(item.category or "", 
                                         str(item.quantity) if item.quantity else "",
                                         item.unit or "",
                                         supplier_name,
                                         date_str))
    
    def _refresh_projects(self):
        """Refresh the projects list."""
        # Clear existing projects
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
        
        # Load projects
        projects = self.project_controller.get_all_projects()
        
        for project in projects:
            date_str = format_date_display(project.date_created) if project.date_created else ""
            materials_count = len(project.materials_used)
            
            self.projects_tree.insert("", tk.END, text=str(project.id),
                                     values=(project.description or "",
                                            date_str,
                                            str(materials_count)))
    
    def _refresh_suppliers(self):
        """Refresh the suppliers list."""
        # Clear existing suppliers
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
        
        # Load suppliers
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
            self.item_controller.create_item(**item_data)
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
            self.item_controller.update_item(item_id, **item_data)
            messagebox.showinfo("Success", "Item updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update item: {str(e)}")
    
    def _new_project(self):
        """Open form to create a new project."""
        items = self.db.items.get_all_items()
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
        
        items = self.db.items.get_all_items()
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
            project_id = self.project_controller.create_project(
                name=project_data['name'],
                description=project_data['description'],
                date_created=project_data['date_created']
            )
            # Add materials
            for item_id, quantity in project_data['materials_used']:
                self.project_controller.add_material_to_project(project_id, item_id, quantity)
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
            messagebox.showinfo("Success", "Project updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update project: {str(e)}")
    
    def _new_supplier(self):
        """Open simple dialog to create a new supplier."""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Supplier")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("400x200")
        
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Name *:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=name_var, width=40).grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Contact Info *:").grid(row=1, column=0, sticky=tk.W, pady=5)
        contact_var = tk.StringVar()
        ttk.Entry(frame, textvariable=contact_var, width=40).grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Website:").grid(row=2, column=0, sticky=tk.W, pady=5)
        website_var = tk.StringVar()
        ttk.Entry(frame, textvariable=website_var, width=40).grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="Notes:").grid(row=3, column=0, sticky=tk.W, pady=5)
        notes_text = tk.Text(frame, width=40, height=3)
        notes_text.grid(row=3, column=1, pady=5)
        
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
        
        ttk.Button(frame, text="Save", command=save).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Cancel", command=dialog.destroy).grid(row=4, column=1, pady=10, sticky=tk.E)
    
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
    
    def run(self):
        """Start the main event loop."""
        self.root.mainloop()

