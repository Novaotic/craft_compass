"""Import dialog for CSV and JSON import."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controllers.export_controller import ExportController
from typing import Optional


class ImportDialog:
    def __init__(self, parent, export_controller: ExportController):
        """
        Initialize the import dialog.
        
        Args:
            parent: Parent window
            export_controller: ExportController instance (handles import too)
        """
        self.parent = parent
        self.export_controller = export_controller
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Import Data")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.minsize(450, 250)
        self.dialog.geometry("450x250")
        
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
        """Create import dialog widgets."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="Import File", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        self.path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.path_var, width=40).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Browse", command=self._browse_file).pack(side=tk.LEFT, padx=5)
        
        # Conflict resolution
        conflict_frame = ttk.LabelFrame(main_frame, text="Conflict Resolution", padding="10")
        conflict_frame.pack(fill=tk.X, pady=5)
        
        self.conflict_var = tk.StringVar(value="skip")
        ttk.Radiobutton(conflict_frame, text="Skip duplicates", variable=self.conflict_var, value="skip").pack(anchor=tk.W)
        ttk.Radiobutton(conflict_frame, text="Update existing", variable=self.conflict_var, value="update").pack(anchor=tk.W)
        ttk.Radiobutton(conflict_frame, text="Rename new items", variable=self.conflict_var, value="rename").pack(anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Import", command=self._import).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _browse_file(self):
        """Open file browser for import file."""
        filename = filedialog.askopenfilename(
            title="Select Import File",
            filetypes=[
                ("JSON files", "*.json"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.path_var.set(filename)
    
    def _import(self):
        """Perform the import."""
        file_path = self.path_var.get().strip()
        if not file_path:
            messagebox.showwarning("Warning", "Please select a file to import")
            return
        
        conflict_resolution = self.conflict_var.get()
        
        try:
            if file_path.lower().endswith('.json'):
                imported, skipped, errors = self.export_controller.import_from_json(file_path, conflict_resolution)
            elif file_path.lower().endswith('.csv'):
                imported, skipped, errors = self.export_controller.import_items_csv(file_path, conflict_resolution)
            else:
                messagebox.showerror("Error", "Unsupported file format. Please select a JSON or CSV file.")
                return
            
            message = f"Import completed!\n\nImported: {imported}\nSkipped: {skipped}"
            if errors:
                message += f"\n\nErrors: {len(errors)}"
                if len(errors) <= 10:
                    message += "\n" + "\n".join(errors)
                else:
                    message += f"\n(First 10 errors shown)\n" + "\n".join(errors[:10])
            
            messagebox.showinfo("Import Complete", message)
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import data: {str(e)}")

