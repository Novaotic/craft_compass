"""Import service for CSV and JSON formats."""
import csv
import json
from typing import List, Dict, Any, Optional, Tuple
from database.database import CraftCompassDB


def import_items_from_csv(db: CraftCompassDB, file_path: str, conflict_resolution: str = 'skip') -> Tuple[int, int, List[str]]:
    """
    Import items from CSV file.
    
    Args:
        db: CraftCompassDB instance
        file_path: Path to CSV file
        conflict_resolution: How to handle conflicts ('skip', 'update', 'rename')
    
    Returns:
        Tuple of (imported_count, skipped_count, errors)
    """
    imported = 0
    skipped = 0
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 is header)
                try:
                    name = row.get('name', '').strip()
                    if not name:
                        errors.append(f"Row {row_num}: Missing required field 'name'")
                        skipped += 1
                        continue
                    
                    # Check if item exists (by name)
                    existing_items = db.items.get_all_items()
                    existing = next((item for item in existing_items if item['name'] == name), None)
                    
                    item_updated = False
                    if existing:
                        if conflict_resolution == 'skip':
                            skipped += 1
                            continue
                        elif conflict_resolution == 'update':
                            item_id = existing['id']
                            # Handle supplier lookup
                            supplier_id = None
                            supplier_name = row.get('supplier', '').strip()
                            if supplier_name:
                                suppliers = db.suppliers.get_all_suppliers()
                                supplier = next((s for s in suppliers if s['name'] == supplier_name), None)
                                if supplier:
                                    supplier_id = supplier['id']
                            
                            db.items.update_item(
                                item_id=item_id,
                                category=row.get('category', '').strip() or None,
                                quantity=float(row.get('quantity', 0)) if row.get('quantity') else None,
                                unit=row.get('unit', '').strip() or None,
                                supplier_id=supplier_id,
                                purchase_date=row.get('purchase_date', '').strip() or None,
                                photo_path=row.get('photo_path', '').strip() or None
                            )
                            imported += 1
                            item_updated = True
                        elif conflict_resolution == 'rename':
                            # Find unique name
                            counter = 1
                            new_name = f"{name} ({counter})"
                            while next((item for item in existing_items if item['name'] == new_name), None):
                                counter += 1
                                new_name = f"{name} ({counter})"
                            name = new_name
                    
                    # Only add item if it wasn't updated
                    if not item_updated:
                        # Handle supplier lookup
                        supplier_id = None
                        supplier_name = row.get('supplier', '').strip()
                        if supplier_name:
                            suppliers = db.suppliers.get_all_suppliers()
                            supplier = next((s for s in suppliers if s['name'] == supplier_name), None)
                            if supplier:
                                supplier_id = supplier['id']
                        
                        # Add item
                        db.items.add_item(
                            name=name,
                            category=row.get('category', '').strip() or None,
                            quantity=float(row.get('quantity', 0)) if row.get('quantity') else None,
                            unit=row.get('unit', '').strip() or None,
                            supplier_id=supplier_id,
                            purchase_date=row.get('purchase_date', '').strip() or None,
                            photo_path=row.get('photo_path', '').strip() or None
                        )
                        imported += 1
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
                    skipped += 1
    except Exception as e:
        errors.append(f"File error: {str(e)}")
    
    return imported, skipped, errors


def import_from_json(db: CraftCompassDB, file_path: str, conflict_resolution: str = 'skip') -> Tuple[int, int, List[str]]:
    """
    Import data from JSON backup file.
    
    Args:
        db: CraftCompassDB instance
        file_path: Path to JSON file
        conflict_resolution: How to handle conflicts ('skip', 'update', 'rename')
    
    Returns:
        Tuple of (imported_count, skipped_count, errors)
    """
    imported = 0
    skipped = 0
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        export_data = data.get('data', {})
        
        # Import suppliers first
        suppliers_data = export_data.get('suppliers', [])
        supplier_id_map = {}  # Map old IDs to new IDs
        for supplier in suppliers_data:
            try:
                old_id = supplier.get('id')
                existing = db.suppliers.get_supplier_by_id(old_id) if old_id else None
                
                if existing and conflict_resolution == 'skip':
                    supplier_id_map[old_id] = old_id
                    skipped += 1
                    continue
                
                supplier_id = db.suppliers.add_supplier(
                    name=supplier.get('name', ''),
                    contact_info=supplier.get('contact_info', ''),
                    website=supplier.get('website'),
                    notes=supplier.get('notes')
                )
                if old_id:
                    supplier_id_map[old_id] = supplier_id
                imported += 1
            except Exception as e:
                errors.append(f"Supplier {supplier.get('name', 'unknown')}: {str(e)}")
                skipped += 1
        
        # Import items
        items_data = export_data.get('items', [])
        item_id_map = {}
        for item in items_data:
            try:
                old_id = item.get('id')
                supplier_id = supplier_id_map.get(item.get('supplier_id')) if item.get('supplier_id') else None
                
                item_id = db.items.add_item(
                    name=item.get('name', ''),
                    category=item.get('category'),
                    quantity=item.get('quantity'),
                    unit=item.get('unit'),
                    supplier_id=supplier_id,
                    purchase_date=item.get('purchase_date'),
                    photo_path=item.get('photo_path')
                )
                if old_id:
                    item_id_map[old_id] = item_id
                imported += 1
            except Exception as e:
                errors.append(f"Item {item.get('name', 'unknown')}: {str(e)}")
                skipped += 1
        
        # Import tags
        tags_data = export_data.get('tags', [])
        tag_id_map = {}
        for tag in tags_data:
            try:
                old_id = tag.get('id')
                tag_id = db.tags.add_tag(
                    name=tag.get('name', ''),
                    color=tag.get('color')
                )
                if old_id:
                    tag_id_map[old_id] = tag_id
                imported += 1
            except Exception as e:
                errors.append(f"Tag {tag.get('name', 'unknown')}: {str(e)}")
                skipped += 1
        
        # Import item tags
        item_tags = export_data.get('item_tags', {})
        for old_item_id, tag_ids in item_tags.items():
            new_item_id = item_id_map.get(int(old_item_id))
            if new_item_id:
                for old_tag_id in tag_ids:
                    new_tag_id = tag_id_map.get(int(old_tag_id))
                    if new_tag_id:
                        try:
                            db.tags.add_tag_to_item(new_item_id, new_tag_id)
                        except Exception as e:
                            errors.append(f"Item tag association: {str(e)}")
        
        # Import projects
        projects_data = export_data.get('projects', [])
        project_id_map = {}
        for project in projects_data:
            try:
                old_id = project.get('id')
                project_id = db.projects.add_project(
                    name=project.get('name', ''),
                    description=project.get('description'),
                    date_created=project.get('date_created')
                )
                if old_id:
                    project_id_map[old_id] = project_id
                imported += 1
            except Exception as e:
                errors.append(f"Project {project.get('name', 'unknown')}: {str(e)}")
                skipped += 1
        
        # Import project materials
        project_materials = export_data.get('project_materials', {})
        for old_project_id, materials in project_materials.items():
            new_project_id = project_id_map.get(int(old_project_id))
            if new_project_id:
                for material in materials:
                    old_item_id = material.get('item_id')
                    new_item_id = item_id_map.get(int(old_item_id)) if old_item_id else None
                    if new_item_id:
                        try:
                            db.materials.add_project_material(
                                new_project_id,
                                new_item_id,
                                material.get('quantity_used', 0)
                            )
                        except Exception as e:
                            errors.append(f"Project material: {str(e)}")
        
        # Import project tags
        project_tags = export_data.get('project_tags', {})
        for old_project_id, tag_ids in project_tags.items():
            new_project_id = project_id_map.get(int(old_project_id))
            if new_project_id:
                for old_tag_id in tag_ids:
                    new_tag_id = tag_id_map.get(int(old_tag_id))
                    if new_tag_id:
                        try:
                            db.tags.add_tag_to_project(new_project_id, new_tag_id)
                        except Exception as e:
                            errors.append(f"Project tag association: {str(e)}")
        
        # Import item metadata
        item_metadata = export_data.get('item_metadata', {})
        for old_item_id, metadata in item_metadata.items():
            new_item_id = item_id_map.get(int(old_item_id))
            if new_item_id:
                for key, value in metadata.items():
                    try:
                        db.items.add_metadata(new_item_id, key, value)
                    except Exception as e:
                        errors.append(f"Item metadata: {str(e)}")
    
    except Exception as e:
        errors.append(f"File error: {str(e)}")
    
    return imported, skipped, errors

