"""Controller for project-related operations."""
from database.database import CraftCompassDB
from models.project import Project
from typing import List, Optional, Dict, Any


class ProjectController:
    def __init__(self, db: CraftCompassDB):
        """
        Initialize the project controller.
        
        Args:
            db: CraftCompassDB instance
        """
        self.db = db

    def create_project(self, name: str, description: Optional[str] = None,
                       date_created: Optional[str] = None) -> int:
        """
        Create a new project.
        
        Args:
            name: Project name (required)
            description: Project description
            date_created: Creation date (YYYY-MM-DD format)
        
        Returns:
            ID of the created project
        """
        return self.db.projects.add_project(
            name=name,
            description=description,
            date_created=date_created
        )

    def get_project(self, project_id: int) -> Optional[Project]:
        """
        Get a project by ID with its materials.
        
        Args:
            project_id: Project ID
        
        Returns:
            Project object with materials or None if not found
        """
        data = self.db.projects.get_project_by_id(project_id)
        if data:
            project = Project.from_dict(data)
            # Load materials for this project
            materials = self.db.materials.get_materials_by_project(project_id)
            for mat in materials:
                project.add_material(mat['item_id'], mat['quantity_used'])
            return project
        return None

    def get_all_projects(self) -> List[Project]:
        """
        Get all projects.
        
        Returns:
            List of Project objects
        """
        projects_data = self.db.projects.get_all_projects()
        projects = []
        for proj_data in projects_data:
            project = Project.from_dict(proj_data)
            # Load materials for each project
            materials = self.db.materials.get_materials_by_project(proj_data['id'])
            for mat in materials:
                project.add_material(mat['item_id'], mat['quantity_used'])
            projects.append(project)
        return projects

    def update_project(self, project_id: int, name: Optional[str] = None,
                       description: Optional[str] = None, date_created: Optional[str] = None):
        """
        Update a project.
        
        Args:
            project_id: ID of project to update
            name: New name
            description: New description
            date_created: New creation date
        """
        self.db.projects.update_project(
            project_id=project_id,
            name=name,
            description=description,
            date_created=date_created
        )

    def delete_project(self, project_id: int):
        """
        Delete a project and its materials.
        
        Args:
            project_id: ID of project to delete
        """
        # Delete all materials for this project first
        materials = self.db.materials.get_materials_by_project(project_id)
        for mat in materials:
            self.db.materials.delete_project_material(mat['id'])
        # Then delete the project
        self.db.projects.delete_project(project_id)

    def add_material_to_project(self, project_id: int, item_id: int, quantity_used: float) -> int:
        """
        Add a material to a project.
        
        Args:
            project_id: Project ID
            item_id: Item ID
            quantity_used: Quantity used
        
        Returns:
            ID of the created project material
        """
        return self.db.materials.add_project_material(project_id, item_id, quantity_used)

    def remove_material_from_project(self, material_id: int):
        """
        Remove a material from a project.
        
        Args:
            material_id: Project material ID
        """
        self.db.materials.delete_project_material(material_id)

    def get_project_materials(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Get all materials for a project.
        
        Args:
            project_id: Project ID
        
        Returns:
            List of material dictionaries
        """
        return self.db.materials.get_materials_by_project(project_id)
    
    def search_projects(self, search_term: str) -> List[Project]:
        """
        Search projects by name or description.
        
        Args:
            search_term: Search term to match against
        
        Returns:
            List of Project objects matching the search
        """
        projects_data = self.db.projects.search_projects(search_term)
        projects = []
        for proj_data in projects_data:
            project = Project.from_dict(proj_data)
            # Load materials for each project
            materials = self.db.materials.get_materials_by_project(proj_data['id'])
            for mat in materials:
                project.add_material(mat['item_id'], mat['quantity_used'])
            projects.append(project)
        return projects
    
    def filter_projects(self, date_from: Optional[str] = None, date_to: Optional[str] = None,
                       min_materials: Optional[int] = None) -> List[Project]:
        """
        Filter projects by date range or material count.
        
        Args:
            date_from: Filter by creation date from (YYYY-MM-DD)
            date_to: Filter by creation date to (YYYY-MM-DD)
            min_materials: Minimum number of materials
        
        Returns:
            List of Project objects matching the filters
        """
        projects_data = self.db.projects.filter_projects(
            date_from=date_from,
            date_to=date_to,
            min_materials=min_materials
        )
        projects = []
        for proj_data in projects_data:
            project = Project.from_dict(proj_data)
            # Load materials for each project
            materials = self.db.materials.get_materials_by_project(proj_data['id'])
            for mat in materials:
                project.add_material(mat['item_id'], mat['quantity_used'])
            projects.append(project)
        return projects

