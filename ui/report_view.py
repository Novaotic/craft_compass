"""Report view for displaying statistics."""
import tkinter as tk
from tkinter import ttk
from controllers.report_controller import ReportController


class ReportView(ttk.Frame):
    def __init__(self, parent, report_controller: ReportController):
        """
        Initialize the report view.
        
        Args:
            parent: Parent widget
            report_controller: ReportController instance
        """
        super().__init__(parent)
        self.report_controller = report_controller
        self._create_widgets()
        self.refresh()
    
    def _create_widgets(self):
        """Create report widgets."""
        # Title
        title_label = ttk.Label(self, text="Inventory Summary", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Summary frame
        summary_frame = ttk.LabelFrame(self, text="Statistics", padding="10")
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_text = tk.Text(summary_frame, height=10, width=60, wrap=tk.WORD)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Refresh button
        ttk.Button(self, text="Refresh", command=self.refresh).pack(pady=5)
    
    def refresh(self):
        """Refresh the report data."""
        try:
            summary = self.report_controller.get_inventory_summary()
            
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert('1.0', "Inventory Summary\n")
            self.stats_text.insert(tk.END, "=" * 50 + "\n\n")
            self.stats_text.insert(tk.END, f"Total Items: {summary['total_items']}\n")
            self.stats_text.insert(tk.END, f"Total Suppliers: {summary['total_suppliers']}\n")
            self.stats_text.insert(tk.END, f"Total Projects: {summary['total_projects']}\n\n")
            self.stats_text.insert(tk.END, "Items by Category:\n")
            self.stats_text.insert(tk.END, "-" * 50 + "\n")
            
            if summary['categories']:
                for category, count in sorted(summary['categories'].items()):
                    self.stats_text.insert(tk.END, f"  {category}: {count}\n")
            else:
                self.stats_text.insert(tk.END, "  No items yet\n")
        except Exception as e:
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert('1.0', f"Error loading report: {str(e)}")

