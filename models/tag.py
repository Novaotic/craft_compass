class Tag:
    def __init__(self, name: str, tag_id: int = None, color: str = None):
        self.id = tag_id
        self.name = name
        self.color = color  # Hex color code or color name
    
    def to_dict(self):
        """Convert the tag to a dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a Tag instance from a dictionary (e.g., from database)."""
        return cls(
            tag_id=data.get('id'),
            name=data.get('name'),
            color=data.get('color')
        )

