"""Metadata editor dialog for custom item metadata."""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, Dict
from database.database import CraftCompassDB


class MetadataForm:
    def __init__(self, parent, db: CraftCompassDB, item_id: int, on_save: Optional[Callable] = None):
        """
        Initialize the metadata form dialog.
        
        Args:
            parent: Parent window
            db: CraftCompassDB instance
            item_id: ID of the item to edit metadata for
            on_save: Callback function called when metadata is saved
        """
        self.parent = parent
        self.db = db
        self.item_id = item_id
        self.on_save = on_save
        self.metadata_items = []  # List of (key, value) tuples
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Metadata")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.minsize(500, 400)
        self.dialog.geometry("500x400")
        
        self._create_widgets()
        self._load_metadata()
        self._center_window()
    
    def _center_window(self):
        """Center the dialog window."""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_reqwidth()
        height = self.dialog.winfo_reqheight()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Create metadata editor widgets."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        info_label = ttk.Label(main_frame, text="Add custom key-value pairs for this item:", font=("Arial", 9))
        info_label.pack(pady=5)
        
        # Metadata list
        list_frame = ttk.LabelFrame(main_frame, text="Metadata", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview with scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.metadata_tree = ttk.Treeview(list_frame, columns=("Value",), show="headings", yscrollcommand=scrollbar.set)
        self.metadata_tree.heading("#0", text="Key")
        self.metadata_tree.heading("Value", text="Value")
        self.metadata_tree.column("#0", width=200)
        self.metadata_tree.column("Value", width=250)
        self.metadata_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.metadata_tree.yview)
        
        # Add metadata controls
        add_frame = ttk.Frame(main_frame)
        add_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(add_frame, text="Key:").pack(side=tk.LEFT, padx=5)
        self.key_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.key_var, width=20).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(add_frame, text="Value:").pack(side=tk.LEFT, padx=5)
        self.value_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.value_var, width=20).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(add_frame, text="Add", command=self._add_metadata).pack(side=tk.LEFT, padx=5)
        ttk.Button(add_frame, text="Remove", command=self._remove_metadata).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Save", command=self._save_metadata).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _load_metadata(self):
        """Load existing metadata."""
        metadata_list = self.db.items.get_metadata(self.item_id)
        for meta in metadata_list:
            key = meta.get('key', '')
            value = meta.get('value', '')
            self.metadata_items.append((key, value))
            self.metadata_tree.insert("", tk.END, text=key, values=(value,))
    
    def _add_metadata(self):
        """Add a new metadata entry."""
        key = self.key_var.get().strip()
        value = self.value_var.get().strip()
        
        if not key:
            messagebox.showwarning("Warning", "Key is required")
            return
        
        # Check if key already exists
        for existing_key, _ in self.metadata_items:
            if existing_key == key:
                messagebox.showwarning("Warning", f"Key '{key}' already exists")
                return
        
        self.metadata_items.append((key, value))
        self.metadata_tree.insert("", tk.END, text=key, values=(value,))
        self.key_var.set("")
        self.value_var.set("")
    
    def _remove_metadata(self):
        """Remove selected metadata entry."""
        selection = self.metadata_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a metadata entry to remove")
            return
        
        key = self.metadata_tree.item(selection[0])['text']
        self.metadata_tree.delete(selection[0])
        self.metadata_items = [(k, v) for k, v in self.metadata_items if k != key]
    
    def _save_metadata(self):
        """Save metadata to database."""
        try:
            # Get current metadata keys
            current_metadata = self.db.items.get_metadata(self.item_id)
            current_keys = {meta['key'] for meta in current_metadata}
            
            # Update or add new metadata
            new_keys = {key for key, _ in self.metadata_items}
            
            # Remove deleted keys
            for key in current_keys - new_keys:
                self.db.items.delete_metadata(self.item_id, key)
            
            # Add or update metadata
            for key, value in self.metadata_items:
                self.db.items.add_metadata(self.item_id, key, value)
            
            messagebox.showinfo("Success", "Metadata saved successfully")
            if self.on_save:
                self.on_save()
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save metadata: {str(e)}")

