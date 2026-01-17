"""Image management utility functions."""
import os
import shutil
from typing import Optional, Tuple
from pathlib import Path


def get_images_directory(project_root: Optional[str] = None) -> str:
    """
    Get the images storage directory path.
    
    Args:
        project_root: Root directory of the project. If None, uses current working directory.
    
    Returns:
        Path to images directory
    """
    if project_root is None:
        project_root = os.getcwd()
    images_dir = os.path.join(project_root, 'data', 'images')
    os.makedirs(images_dir, exist_ok=True)
    return images_dir


def copy_image_to_storage(source_path: str, project_root: Optional[str] = None) -> str:
    """
    Copy an image file to the application's image storage directory.
    
    Args:
        source_path: Path to source image file
        project_root: Root directory of the project
    
    Returns:
        Relative path to the stored image (for database storage)
    """
    if not os.path.isfile(source_path):
        raise FileNotFoundError(f"Image file not found: {source_path}")
    
    images_dir = get_images_directory(project_root)
    filename = os.path.basename(source_path)
    
    # Handle filename conflicts
    dest_path = os.path.join(images_dir, filename)
    counter = 1
    base_name, ext = os.path.splitext(filename)
    while os.path.exists(dest_path):
        new_filename = f"{base_name}_{counter}{ext}"
        dest_path = os.path.join(images_dir, new_filename)
        counter += 1
    
    shutil.copy2(source_path, dest_path)
    
    # Return relative path for database storage
    return os.path.join('data', 'images', os.path.basename(dest_path))


def get_image_path(relative_path: str, project_root: Optional[str] = None) -> str:
    """
    Get absolute path from relative image path.
    
    Args:
        relative_path: Relative path stored in database
        project_root: Root directory of the project
    
    Returns:
        Absolute path to image file
    """
    if project_root is None:
        project_root = os.getcwd()
    
    if os.path.isabs(relative_path):
        return relative_path
    
    return os.path.join(project_root, relative_path)


def validate_image(file_path: str, max_size_mb: float = 10.0) -> Tuple[bool, Optional[str]]:
    """
    Validate an image file.
    
    Args:
        file_path: Path to image file
        max_size_mb: Maximum file size in MB
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not os.path.isfile(file_path):
        return False, "File does not exist"
    
    # Check file size
    file_size = os.path.getsize(file_path)
    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        return False, f"File size exceeds {max_size_mb}MB limit"
    
    # Check file extension
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in valid_extensions:
        return False, f"Invalid image format. Supported: {', '.join(valid_extensions)}"
    
    return True, None


def resize_image(file_path: str, max_width: int = 800, max_height: int = 600, 
                 project_root: Optional[str] = None) -> Optional[str]:
    """
    Resize an image (requires Pillow if available, otherwise returns original path).
    
    Args:
        file_path: Path to image file
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        project_root: Root directory of the project
    
    Returns:
        Path to resized image (or original if Pillow not available)
    """
    try:
        from PIL import Image
        
        img = Image.open(file_path)
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Save to thumbnail directory
        images_dir = get_images_directory(project_root)
        thumb_dir = os.path.join(images_dir, 'thumbnails')
        os.makedirs(thumb_dir, exist_ok=True)
        
        filename = os.path.basename(file_path)
        thumb_path = os.path.join(thumb_dir, filename)
        img.save(thumb_path)
        
        return os.path.join('data', 'images', 'thumbnails', filename)
    except ImportError:
        # Pillow not available, return original
        return None
    except Exception:
        # Error resizing, return original
        return None

