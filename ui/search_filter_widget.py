"""Reusable search and filter widget component."""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Dict, Any


class SearchFilterWidget(ttk.Frame):
    def __init__(self, parent, on_search: Optional[Callable] = None, 
                 on_filter: Optional[Callable] = None, filter_options: Optional[Dict[str, list]] = None):
        """
        Initialize the search/filter widget.
        
        Args:
            parent: Parent widget
            on_search: Callback function called when search text changes
            on_filter: Callback function called when filters change
            filter_options: Dictionary of filter options {filter_name: [option_list]}
        """
        super().__init__(parent)
        self.on_search = on_search
        self.on_filter = on_filter
        self.filter_options = filter_options or {}
        self.filter_vars = {}
        self._search_debounce_id = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create search and filter widgets."""
        # Search frame
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_change)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(search_frame, text="Clear", command=self._clear_search).pack(side=tk.LEFT, padx=5)
        
        # Filter frame
        if self.filter_options:
            filter_frame = ttk.LabelFrame(self, text="Filters", padding="5")
            filter_frame.pack(fill=tk.X, padx=5, pady=5)
            
            row = 0
            col = 0
            for filter_name, options in self.filter_options.items():
                if col > 2:  # Start new row after 3 filters
                    row += 1
                    col = 0
                
                frame = ttk.Frame(filter_frame)
                frame.grid(row=row, column=col, padx=5, pady=5, sticky=tk.W)
                
                ttk.Label(frame, text=f"{filter_name}:").pack(side=tk.LEFT, padx=2)
                var = tk.StringVar()
                var.set("All")
                var.trace('w', self._on_filter_change)
                self.filter_vars[filter_name] = var
                
                combo = ttk.Combobox(frame, textvariable=var, width=15, state="readonly")
                combo['values'] = ["All"] + options
                combo.pack(side=tk.LEFT, padx=2)
                
                col += 1
            
            # Clear filters button
            ttk.Button(filter_frame, text="Clear All Filters", command=self._clear_filters).grid(
                row=row+1, column=0, columnspan=3, pady=5
            )
    
    def _on_search_change(self, *args):
        """Handle search text change with debouncing."""
        if self._search_debounce_id:
            self.after_cancel(self._search_debounce_id)
        
        # Debounce: wait 300ms before calling callback
        self._search_debounce_id = self.after(300, self._trigger_search)
    
    def _trigger_search(self):
        """Trigger the search callback."""
        if self.on_search:
            search_term = self.search_var.get().strip()
            self.on_search(search_term)
    
    def _on_filter_change(self, *args):
        """Handle filter change."""
        if self.on_filter:
            filters = {}
            for filter_name, var in self.filter_vars.items():
                value = var.get()
                if value != "All":
                    filters[filter_name] = value
            self.on_filter(filters)
    
    def _clear_search(self):
        """Clear search field."""
        self.search_var.set("")
        if self.on_search:
            self.on_search("")
    
    def _clear_filters(self):
        """Clear all filters."""
        for var in self.filter_vars.values():
            var.set("All")
        if self.on_filter:
            self.on_filter({})
    
    def get_search_term(self) -> str:
        """Get current search term."""
        return self.search_var.get().strip()
    
    def get_filters(self) -> Dict[str, str]:
        """Get current filter values."""
        filters = {}
        for filter_name, var in self.filter_vars.items():
            value = var.get()
            if value != "All":
                filters[filter_name] = value
        return filters

