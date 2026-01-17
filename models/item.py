class Item:
    def __init__(self, name, category=None, quantity=None, unit=None, supplier_id=None, 
                 purchase_date=None, photo_path=None, item_id=None):
        self.id = item_id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.unit = unit  # e.g., grams, meters, feet
        self.supplier_id = supplier_id  # supplier ID reference
        self.purchase_date = purchase_date
        self.photo_path = photo_path  # path to an image file of the item

    def to_dict(self):
        """Convert the item to a dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'quantity': self.quantity,
            'unit': self.unit,
            'supplier_id': self.supplier_id,
            'purchase_date': self.purchase_date,
            'photo_path': self.photo_path
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create an Item instance from a dictionary (e.g., from database)."""
        return cls(
            item_id=data.get('id'),
            name=data.get('name'),
            category=data.get('category'),
            quantity=data.get('quantity'),
            unit=data.get('unit'),
            supplier_id=data.get('supplier_id'),
            purchase_date=data.get('purchase_date'),
            photo_path=data.get('photo_path')
        )
