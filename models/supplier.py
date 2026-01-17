class Supplier:
    def __init__(self, name, contact_info, website=None, notes=None):
        self.name = name
        self.contact_info = contact_info
        self.website = website
        self.notes = notes

    def to_dict(self):
        """Convert the supplier to a dictionary representation."""
        return vars(self)