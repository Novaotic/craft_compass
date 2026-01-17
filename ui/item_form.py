"""Form dialog for creating/editing items."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Callable, List
from utils.validators import validate_required, validate_date, validate_quantity, validate_integer
from utils.helpers import get_today_date
from utils.image_helpers import validate_image, copy_image_to_storage, get_image_path
from controllers.tag_controller import TagController
import os


class ItemForm:
    def __init__(self, parent, db, suppliers_list, on_save: Optional[Callable] = None, item_data: Optional[dict] = None):
        """
        Initialize the item form dialog.
        
        Args:
            parent: Parent window
            db: CraftCompassDB instance
            suppliers_list: List of supplier dictionaries for dropdown
            on_save: Callback function called when item is saved
            item_data: Optional item data for editing (if None, creates new item)
        """
        self.parent = parent
        self.db = db
        self.suppliers_list = suppliers_list
        self.on_save = on_save
        self.item_data = item_data
        self.result = None
        self.tag_controller = TagController(db)
        self.selected_tag_ids = []
        self.item_id = item_data.get('id') if item_data else None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Item" if item_data else "New Item")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Set minimum size and initial geometry
        self.dialog.minsize(550, 550)
        self.dialog.geometry("550x550")
        
        self._create_widgets()
        if item_data:
            self._load_item_data()
        
        # Center the dialog after widgets are created
        self._center_window()
    
    def _center_window(self):
        """Center the dialog window on the parent."""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_reqwidth()
        height = self.dialog.winfo_reqheight()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Create form widgets."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for proper resizing
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Name field
        ttk.Label(main_frame, text="Name *:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var, width=40).grid(row=0, column=1, pady=5, padx=5, sticky=tk.W+tk.E)
        
        # Category field
        ttk.Label(main_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.category_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.category_var, width=40).grid(row=1, column=1, pady=5, padx=5, sticky=tk.W+tk.E)
        
        # Quantity field
        ttk.Label(main_frame, text="Quantity:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        quantity_frame = ttk.Frame(main_frame)
        quantity_frame.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        self.quantity_var = tk.StringVar()
        ttk.Entry(quantity_frame, textvariable=self.quantity_var, width=20).pack(side=tk.LEFT)
        self.unit_var = tk.StringVar()
        unit_entry = ttk.Entry(quantity_frame, textvariable=self.unit_var, width=15)
        unit_entry.pack(side=tk.LEFT, padx=5)
        
        # Supplier field
        ttk.Label(main_frame, text="Supplier:").grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.supplier_var = tk.StringVar()
        supplier_combo = ttk.Combobox(main_frame, textvariable=self.supplier_var, width=37, state="readonly")
        supplier_combo['values'] = [""] + [f"{s['id']}: {s['name']}" for s in self.suppliers_list]
        supplier_combo.grid(row=3, column=1, pady=5, padx=5, sticky=tk.W+tk.E)
        self.supplier_combo = supplier_combo
        
        # Purchase date field
        ttk.Label(main_frame, text="Purchase Date:").grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        date_frame = ttk.Frame(main_frame)
        date_frame.grid(row=4, column=1, pady=5, padx=5, sticky=tk.W)
        self.purchase_date_var = tk.StringVar()
        ttk.Entry(date_frame, textvariable=self.purchase_date_var, width=20).pack(side=tk.LEFT)
        ttk.Button(date_frame, text="Today", command=self._set_today_date).pack(side=tk.LEFT, padx=5)
        
        # Photo path field with preview
        ttk.Label(main_frame, text="Photo Path:").grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)
        photo_frame = ttk.Frame(main_frame)
        photo_frame.grid(row=5, column=1, pady=5, padx=5, sticky=tk.W+tk.E)
        self.photo_path_var = tk.StringVar()
        self.photo_path_var.trace('w', self._update_image_preview)
        photo_entry = ttk.Entry(photo_frame, textvariable=self.photo_path_var, width=30)
        photo_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(photo_frame, text="Browse", command=self._browse_photo).pack(side=tk.LEFT, padx=5)
        
        # Image preview
        self.image_preview_label = ttk.Label(main_frame, text="No image")
        self.image_preview_label.grid(row=6, column=0, columnspan=2, pady=5, padx=5)
        
        # Tags field
        ttk.Label(main_frame, text="Tags:").grid(row=7, column=0, sticky=tk.W+tk.N, pady=5, padx=5)
        tags_frame = ttk.Frame(main_frame)
        tags_frame.grid(row=7, column=1, pady=5, padx=5, sticky=tk.W+tk.E)
        
        # Tags listbox with scrollbar
        tags_list_frame = ttk.Frame(tags_frame)
        tags_list_frame.pack(fill=tk.BOTH, expand=True)
        
        tags_scrollbar = ttk.Scrollbar(tags_list_frame)
        tags_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tags_listbox = tk.Listbox(tags_list_frame, height=4, selectmode=tk.MULTIPLE, yscrollcommand=tags_scrollbar.set)
        self.tags_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tags_scrollbar.config(command=self.tags_listbox.yview)
        
        # Load tags into listbox
        self._load_tags_list()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="Save", command=self._save_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._cancel).pack(side=tk.LEFT, padx=5)
    
    def _set_today_date(self):
        """Set purchase date to today."""
        self.purchase_date_var.set(get_today_date())
    
    def _browse_photo(self):
        """Open file browser for photo selection."""
        filename = filedialog.askopenfilename(
            title="Select Photo",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"), ("All files", "*.*")]
        )
        if filename:
            # Validate image
            is_valid, error = validate_image(filename)
            if not is_valid:
                messagebox.showerror("Validation Error", error)
                return
            self.photo_path_var.set(filename)
    
    def _update_image_preview(self, *args):
        """Update image preview when path changes."""
        photo_path = self.photo_path_var.get().strip()
        if photo_path and os.path.isfile(photo_path):
            try:
                from PIL import Image, ImageTk
                img = Image.open(photo_path)
                img.thumbnail((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.image_preview_label.config(image=photo, text="")
                self.image_preview_label.image = photo  # Keep a reference
            except ImportError:
                self.image_preview_label.config(text="Image: " + os.path.basename(photo_path))
            except Exception:
                self.image_preview_label.config(text="Invalid image")
        else:
            self.image_preview_label.config(text="No image", image="")
    
    def _load_tags_list(self):
        """Load available tags into the listbox."""
        tags = self.tag_controller.get_all_tags()
        for tag in tags:
            self.tags_listbox.insert(tk.END, f"{tag.name}")
    
    def _load_item_data(self):
        """Load item data into form fields."""
        if not self.item_data:
            return
        
        self.name_var.set(self.item_data.get('name', ''))
        self.category_var.set(self.item_data.get('category', ''))
        self.quantity_var.set(str(self.item_data.get('quantity', '')) if self.item_data.get('quantity') is not None else '')
        self.unit_var.set(self.item_data.get('unit', ''))
        
        supplier_id = self.item_data.get('supplier_id')
        if supplier_id:
            supplier_str = f"{supplier_id}: {next((s['name'] for s in self.suppliers_list if s['id'] == supplier_id), '')}"
            self.supplier_var.set(supplier_str)
        
        self.purchase_date_var.set(self.item_data.get('purchase_date', ''))
        photo_path = self.item_data.get('photo_path', '')
        if photo_path:
            # Try to resolve relative path
            try:
                abs_path = get_image_path(photo_path)
                if os.path.isfile(abs_path):
                    self.photo_path_var.set(abs_path)
                else:
                    self.photo_path_var.set(photo_path)
            except:
                self.photo_path_var.set(photo_path)
        
        # Load tags
        if self.item_id:
            item_tags = self.tag_controller.get_item_tags(self.item_id)
            tag_names = [tag.name for tag in item_tags]
            for i, tag_name in enumerate(self.tags_listbox.get(0, tk.END)):
                if tag_name in tag_names:
                    self.tags_listbox.selection_set(i)
                    self.selected_tag_ids.append(self.tag_controller.get_all_tags()[i].id)
    
    def _save_item(self):
        """Validate and save the item."""
        # Validate name (required)
        is_valid, error = validate_required(self.name_var.get(), "Name")
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        # Validate quantity
        is_valid, error, quantity = validate_quantity(self.quantity_var.get(), "Quantity")
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        # Validate date
        date_str = self.purchase_date_var.get().strip()
        if date_str:
            is_valid, error = validate_date(date_str, "Purchase Date")
            if not is_valid:
                messagebox.showerror("Validation Error", error)
                return
        
        # Parse supplier ID
        supplier_id = None
        supplier_str = self.supplier_var.get()
        if supplier_str:
            try:
                supplier_id = int(supplier_str.split(':')[0])
            except (ValueError, IndexError):
                pass
        
        # Handle image path - copy to storage if it's a new file
        photo_path = self.photo_path_var.get().strip()
        if photo_path and os.path.isfile(photo_path):
            try:
                # Copy to storage if not already in data/images
                if not photo_path.startswith('data/images'):
                    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                    photo_path = copy_image_to_storage(photo_path, project_root)
            except Exception as e:
                messagebox.showwarning("Warning", f"Could not copy image: {str(e)}\nUsing original path.")
        
        # Get selected tags
        selected_indices = self.tags_listbox.curselection()
        all_tags = self.tag_controller.get_all_tags()
        selected_tag_ids = [all_tags[i].id for i in selected_indices]
        
        # Collect form data
        item_data = {
            'name': self.name_var.get().strip(),
            'category': self.category_var.get().strip() or None,
            'quantity': quantity,
            'unit': self.unit_var.get().strip() or None,
            'supplier_id': supplier_id,
            'purchase_date': date_str or None,
            'photo_path': photo_path or None,
            'tag_ids': selected_tag_ids
        }
        
        self.result = item_data
        if self.on_save:
            self.on_save(item_data)
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancel the dialog."""
        self.dialog.destroy()

