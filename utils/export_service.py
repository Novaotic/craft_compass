"""Export service for CSV and JSON formats."""
import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from database.database import CraftCompassDB


def export_items_to_csv(db: CraftCompassDB, file_path: str):
    """
    Export all items to CSV file.
    
    Args:
        db: CraftCompassDB instance
        file_path: Path to save CSV file
    """
    items = db.items.get_all_items()
    suppliers = db.suppliers.get_all_suppliers()
    supplier_dict = {s['id']: s['name'] for s in suppliers}
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        if not items:
            return
        
        fieldnames = ['id', 'name', 'category', 'quantity', 'unit', 'supplier', 'purchase_date', 'photo_path']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in items:
            supplier_name = supplier_dict.get(item['supplier_id'], '') if item.get('supplier_id') else ''
            writer.writerow({
                'id': item.get('id', ''),
                'name': item.get('name', ''),
                'category': item.get('category', ''),
                'quantity': item.get('quantity', ''),
                'unit': item.get('unit', ''),
                'supplier': supplier_name,
                'purchase_date': item.get('purchase_date', ''),
                'photo_path': item.get('photo_path', '')
            })


def export_projects_to_csv(db: CraftCompassDB, file_path: str):
    """
    Export all projects to CSV file.
    
    Args:
        db: CraftCompassDB instance
        file_path: Path to save CSV file
    """
    projects = db.projects.get_all_projects()
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        if not projects:
            return
        
        fieldnames = ['id', 'name', 'description', 'date_created']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for project in projects:
            writer.writerow({
                'id': project.get('id', ''),
                'name': project.get('name', ''),
                'description': project.get('description', ''),
                'date_created': project.get('date_created', '')
            })


def export_suppliers_to_csv(db: CraftCompassDB, file_path: str):
    """
    Export all suppliers to CSV file.
    
    Args:
        db: CraftCompassDB instance
        file_path: Path to save CSV file
    """
    suppliers = db.suppliers.get_all_suppliers()
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        if not suppliers:
            return
        
        fieldnames = ['id', 'name', 'contact_info', 'website', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for supplier in suppliers:
            writer.writerow({
                'id': supplier.get('id', ''),
                'name': supplier.get('name', ''),
                'contact_info': supplier.get('contact_info', ''),
                'website': supplier.get('website', ''),
                'notes': supplier.get('notes', '')
            })


def export_all_to_json(db: CraftCompassDB, file_path: str):
    """
    Export all data to JSON file.
    
    Args:
        db: CraftCompassDB instance
        file_path: Path to save JSON file
    """
    # Get all data
    items = db.items.get_all_items()
    projects = db.projects.get_all_projects()
    suppliers = db.suppliers.get_all_suppliers()
    tags = db.tags.get_all_tags()
    
    # Get project materials
    project_materials = {}
    for project in projects:
        project_id = project['id']
        materials = db.materials.get_materials_by_project(project_id)
        project_materials[project_id] = materials
    
    # Get item tags
    item_tags = {}
    for item in items:
        item_id = item['id']
        tags_list = db.tags.get_item_tags(item_id)
        item_tags[item_id] = [tag['id'] for tag in tags_list]
    
    # Get project tags
    project_tags_dict = {}
    for project in projects:
        project_id = project['id']
        tags_list = db.tags.get_project_tags(project_id)
        project_tags_dict[project_id] = [tag['id'] for tag in tags_list]
    
    # Get item metadata
    item_metadata = {}
    for item in items:
        item_id = item['id']
        metadata_list = db.items.get_metadata(item_id)
        item_metadata[item_id] = {meta['key']: meta['value'] for meta in metadata_list}
    
    # Build export structure
    export_data = {
        'export_date': datetime.now().isoformat(),
        'version': '1.0',
        'data': {
            'suppliers': suppliers,
            'items': items,
            'projects': projects,
            'tags': tags,
            'project_materials': project_materials,
            'item_tags': item_tags,
            'project_tags': project_tags_dict,
            'item_metadata': item_metadata
        }
    }
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)


def create_backup(db: CraftCompassDB, backup_dir: str) -> str:
    """
    Create a full database backup as JSON.
    
    Args:
        db: CraftCompassDB instance
        backup_dir: Directory to save backup
    
    Returns:
        Path to the backup file
    """
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"craft_compass_backup_{timestamp}.json")
    export_all_to_json(db, backup_file)
    return backup_file

