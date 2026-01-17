"""Tag management dialog."""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from controllers.tag_controller import TagController
from models.tag import Tag


class TagManager:
    def __init__(self, parent, tag_controller: TagController, on_update: Optional[Callable] = None):
        """
        Initialize the tag manager dialog.
        
        Args:
            parent: Parent window
            tag_controller: TagController instance
            on_update: Callback function called when tags are updated
        """
        self.parent = parent
        self.tag_controller = tag_controller
        self.on_update = on_update
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Manage Tags")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.minsize(500, 400)
        self.dialog.geometry("500x400")
        
        self._create_widgets()
        self._refresh_tags()
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
        """Create tag management widgets."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add tag section
        add_frame = ttk.LabelFrame(main_frame, text="Add New Tag", padding="10")
        add_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(add_frame, text="Color:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.color_var = tk.StringVar()
        color_combo = ttk.Combobox(add_frame, textvariable=self.color_var, width=28, state="readonly")
        color_combo['values'] = ['', 'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'gray', '#FF0000', '#0000FF', '#00FF00']
        color_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(add_frame, text="Add Tag", command=self._add_tag).grid(row=2, column=0, columnspan=2, pady=10)
        
        add_frame.grid_columnconfigure(1, weight=1)
        
        # Tags list
        list_frame = ttk.LabelFrame(main_frame, text="Existing Tags", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview with scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tags_tree = ttk.Treeview(list_frame, columns=("Color",), show="headings", yscrollcommand=scrollbar.set)
        self.tags_tree.heading("#0", text="ID")
        self.tags_tree.heading("Color", text="Color")
        self.tags_tree.column("#0", width=50)
        self.tags_tree.column("Color", width=150)
        self.tags_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tags_tree.yview)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        ttk.Button(button_frame, text="Delete Selected", command=self._delete_tag).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _add_tag(self):
        """Add a new tag."""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Tag name is required")
            return
        
        try:
            self.tag_controller.create_tag(name=name, color=self.color_var.get().strip() or None)
            messagebox.showinfo("Success", "Tag created successfully")
            self.name_var.set("")
            self.color_var.set("")
            self._refresh_tags()
            if self.on_update:
                self.on_update()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create tag: {str(e)}")
    
    def _delete_tag(self):
        """Delete selected tag."""
        selection = self.tags_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a tag to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this tag?"):
            return
        
        tag_id = int(self.tags_tree.item(selection[0])['text'])
        try:
            self.tag_controller.delete_tag(tag_id)
            messagebox.showinfo("Success", "Tag deleted successfully")
            self._refresh_tags()
            if self.on_update:
                self.on_update()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete tag: {str(e)}")
    
    def _refresh_tags(self):
        """Refresh the tags list."""
        for item in self.tags_tree.get_children():
            self.tags_tree.delete(item)
        
        tags = self.tag_controller.get_all_tags()
        for tag in tags:
            self.tags_tree.insert("", tk.END, text=str(tag.id), values=(tag.color or "",))

