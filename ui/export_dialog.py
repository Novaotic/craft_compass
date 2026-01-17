"""Export dialog for CSV and JSON export."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controllers.export_controller import ExportController
from typing import Optional


class ExportDialog:
    def __init__(self, parent, export_controller: ExportController):
        """
        Initialize the export dialog.
        
        Args:
            parent: Parent window
            export_controller: ExportController instance
        """
        self.parent = parent
        self.export_controller = export_controller
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Export Data")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.minsize(450, 300)
        self.dialog.geometry("450x300")
        
        self._create_widgets()
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
        """Create export dialog widgets."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Export type selection
        type_frame = ttk.LabelFrame(main_frame, text="Export Type", padding="10")
        type_frame.pack(fill=tk.X, pady=5)
        
        self.export_type_var = tk.StringVar(value="all")
        ttk.Radiobutton(type_frame, text="All Data", variable=self.export_type_var, value="all").pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="Items Only", variable=self.export_type_var, value="items").pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="Projects Only", variable=self.export_type_var, value="projects").pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="Suppliers Only", variable=self.export_type_var, value="suppliers").pack(anchor=tk.W)
        
        # Format selection
        format_frame = ttk.LabelFrame(main_frame, text="Format", padding="10")
        format_frame.pack(fill=tk.X, pady=5)
        
        self.format_var = tk.StringVar(value="json")
        ttk.Radiobutton(format_frame, text="JSON (Full Backup)", variable=self.format_var, value="json").pack(anchor=tk.W)
        ttk.Radiobutton(format_frame, text="CSV (Spreadsheet)", variable=self.format_var, value="csv").pack(anchor=tk.W)
        
        # File path
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(path_frame, text="Save to:").pack(side=tk.LEFT, padx=5)
        self.path_var = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.path_var, width=40).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(path_frame, text="Browse", command=self._browse_file).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Export", command=self._export).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _browse_file(self):
        """Open file browser for export location."""
        export_type = self.export_type_var.get()
        format_type = self.format_var.get()
        
        if format_type == "json":
            filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
            default_ext = ".json"
        else:
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
            default_ext = ".csv"
        
        filename = filedialog.asksaveasfilename(
            title="Save Export File",
            defaultextension=default_ext,
            filetypes=filetypes
        )
        if filename:
            self.path_var.set(filename)
    
    def _export(self):
        """Perform the export."""
        file_path = self.path_var.get().strip()
        if not file_path:
            messagebox.showwarning("Warning", "Please select a file path")
            return
        
        export_type = self.export_type_var.get()
        format_type = self.format_var.get()
        
        try:
            if format_type == "json":
                if export_type == "all":
                    self.export_controller.export_all_json(file_path)
                else:
                    messagebox.showwarning("Warning", "JSON export only supports 'All Data'")
                    return
            else:  # CSV
                if export_type == "items":
                    self.export_controller.export_items_csv(file_path)
                elif export_type == "projects":
                    self.export_controller.export_projects_csv(file_path)
                elif export_type == "suppliers":
                    self.export_controller.export_suppliers_csv(file_path)
                else:
                    messagebox.showwarning("Warning", "CSV export requires selecting a specific type")
                    return
            
            messagebox.showinfo("Success", f"Data exported successfully to:\n{file_path}")
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")

