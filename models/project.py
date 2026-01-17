class Project:
    def __init__(self, name, description=None, date_created=None, project_id=None):
        self.id = project_id
        self.name = name
        self.description = description
        self.date_created = date_created
        self.materials_used = []  # List of tuples (item_id, quantity_used)

    def add_material(self, item_id, quantity_used):
        """Add a material to the project with the quantity used."""
        self.materials_used.append((item_id, quantity_used))
    
    def to_dict(self):
        """Convert the project to a dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date_created": self.date_created,
            "materials_used": self.materials_used
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a Project instance from a dictionary (e.g., from database)."""
        project = cls(
            project_id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            date_created=data.get('date_created')
        )
        # Materials will be loaded separately via ProjectMaterialManager
        return project
