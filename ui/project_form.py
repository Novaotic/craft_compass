"""Form dialog for creating/editing projects."""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, List, Dict, Any
from utils.validators import validate_required, validate_date
from utils.helpers import get_today_date


class ProjectForm:
    def __init__(self, parent, db, items_list, on_save: Optional[Callable] = None, project_data: Optional[dict] = None):
        """
        Initialize the project form dialog.
        
        Args:
            parent: Parent window
            db: CraftCompassDB instance
            items_list: List of item dictionaries for material selection
            on_save: Callback function called when project is saved
            project_data: Optional project data for editing (if None, creates new project)
        """
        self.parent = parent
        self.db = db
        self.items_list = items_list
        self.on_save = on_save
        self.project_data = project_data
        self.result = None
        self.selected_materials = []  # List of (item_id, quantity_used) tuples
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Project" if project_data else "New Project")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("600x500")
        self._center_window()
        
        self._create_widgets()
        if project_data:
            self._load_project_data()
    
    def _center_window(self):
        """Center the dialog window on the parent."""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Create form widgets."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Name field
        ttk.Label(main_frame, text="Name *:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var, width=50).grid(row=0, column=1, pady=5, sticky=tk.W)
        
        # Description field
        ttk.Label(main_frame, text="Description:").grid(row=1, column=0, sticky=tk.W+tk.N, pady=5)
        self.description_text = tk.Text(main_frame, width=50, height=4)
        self.description_text.grid(row=1, column=1, pady=5, sticky=tk.W)
        
        # Date created field
        ttk.Label(main_frame, text="Date Created:").grid(row=2, column=0, sticky=tk.W, pady=5)
        date_frame = ttk.Frame(main_frame)
        date_frame.grid(row=2, column=1, pady=5, sticky=tk.W)
        self.date_created_var = tk.StringVar()
        ttk.Entry(date_frame, textvariable=self.date_created_var, width=20).pack(side=tk.LEFT)
        ttk.Button(date_frame, text="Today", command=self._set_today_date).pack(side=tk.LEFT, padx=5)
        
        # Materials section
        ttk.Label(main_frame, text="Materials:").grid(row=3, column=0, sticky=tk.W+tk.N, pady=5)
        materials_frame = ttk.Frame(main_frame)
        materials_frame.grid(row=3, column=1, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Materials listbox with scrollbar
        listbox_frame = ttk.Frame(materials_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.materials_listbox = tk.Listbox(listbox_frame, height=8, yscrollcommand=scrollbar.set)
        self.materials_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.materials_listbox.yview)
        
        # Material selection controls
        material_controls = ttk.Frame(materials_frame)
        material_controls.pack(fill=tk.X, pady=5)
        
        ttk.Label(material_controls, text="Item:").pack(side=tk.LEFT, padx=5)
        self.item_var = tk.StringVar()
        item_combo = ttk.Combobox(material_controls, textvariable=self.item_var, width=30, state="readonly")
        item_combo['values'] = [f"{i['id']}: {i['name']}" for i in self.items_list]
        item_combo.pack(side=tk.LEFT, padx=5)
        self.item_combo = item_combo
        
        ttk.Label(material_controls, text="Qty:").pack(side=tk.LEFT, padx=5)
        self.material_qty_var = tk.StringVar()
        ttk.Entry(material_controls, textvariable=self.material_qty_var, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(material_controls, text="Add", command=self._add_material).pack(side=tk.LEFT, padx=5)
        ttk.Button(material_controls, text="Remove", command=self._remove_material).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="Save", command=self._save_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._cancel).pack(side=tk.LEFT, padx=5)
        
        main_frame.grid_rowconfigure(3, weight=1)
    
    def _set_today_date(self):
        """Set date created to today."""
        self.date_created_var.set(get_today_date())
    
    def _add_material(self):
        """Add a material to the project."""
        item_str = self.item_var.get()
        if not item_str:
            messagebox.showwarning("Warning", "Please select an item")
            return
        
        try:
            item_id = int(item_str.split(':')[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid item selection")
            return
        
        qty_str = self.material_qty_var.get().strip()
        if not qty_str:
            messagebox.showwarning("Warning", "Please enter a quantity")
            return
        
        try:
            quantity = float(qty_str)
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be positive")
                return
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a valid number")
            return
        
        # Check if item already added
        for item_id_existing, _ in self.selected_materials:
            if item_id_existing == item_id:
                messagebox.showwarning("Warning", "Item already added to project")
                return
        
        # Add to list
        self.selected_materials.append((item_id, quantity))
        item_name = next((i['name'] for i in self.items_list if i['id'] == item_id), f"Item {item_id}")
        self.materials_listbox.insert(tk.END, f"{item_name} - {quantity}")
        
        # Clear inputs
        self.item_var.set("")
        self.material_qty_var.set("")
    
    def _remove_material(self):
        """Remove selected material from the project."""
        selection = self.materials_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a material to remove")
            return
        
        index = selection[0]
        self.materials_listbox.delete(index)
        del self.selected_materials[index]
    
    def _load_project_data(self):
        """Load project data into form fields."""
        if not self.project_data:
            return
        
        self.name_var.set(self.project_data.get('name', ''))
        description = self.project_data.get('description', '')
        self.description_text.insert('1.0', description)
        self.date_created_var.set(self.project_data.get('date_created', ''))
        
        # Load materials
        materials = self.project_data.get('materials_used', [])
        for item_id, quantity in materials:
            self.selected_materials.append((item_id, quantity))
            item_name = next((i['name'] for i in self.items_list if i['id'] == item_id), f"Item {item_id}")
            self.materials_listbox.insert(tk.END, f"{item_name} - {quantity}")
    
    def _save_project(self):
        """Validate and save the project."""
        # Validate name (required)
        is_valid, error = validate_required(self.name_var.get(), "Name")
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        # Validate date
        date_str = self.date_created_var.get().strip()
        if date_str:
            is_valid, error = validate_date(date_str, "Date Created")
            if not is_valid:
                messagebox.showerror("Validation Error", error)
                return
        
        # Collect form data
        project_data = {
            'name': self.name_var.get().strip(),
            'description': self.description_text.get('1.0', tk.END).strip() or None,
            'date_created': date_str or None,
            'materials_used': self.selected_materials.copy()
        }
        
        self.result = project_data
        if self.on_save:
            self.on_save(project_data)
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancel the dialog."""
        self.dialog.destroy()

