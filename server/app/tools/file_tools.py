import os
import logging
from typing import Dict, Any, Optional, Union
import json

from app.core.config import settings

logger = logging.getLogger(__name__)

def _is_path_allowed(filepath: str) -> bool:
    """Check if a file path is allowed for access.
    
    Args:
        filepath: Path to check
        
    Returns:
        True if path is allowed, False otherwise
    """
    # Ensure allowed directories are initialized
    if not hasattr(settings, "ALLOWED_FILE_DIRS") or not settings.ALLOWED_FILE_DIRS:
        logger.warning("No allowed file directories configured")
        return False
    
    # Normalize path for platform-independent comparison
    abs_path = os.path.abspath(filepath)
    
    # Check if path is within any allowed directory
    for allowed_dir in settings.ALLOWED_FILE_DIRS:
        allowed_abs = os.path.abspath(allowed_dir)
        if abs_path.startswith(allowed_abs):
            return True
            
    logger.warning(f"Path access denied: {filepath} not in allowed directories")
    return False

def read_file(filepath: str) -> Dict[str, Any]:
    """Read content from a file.
    
    Args:
        filepath: Path to read from (must be in allowed directories)
        
    Returns:
        Dictionary with file content or error
    """
    logger.info(f"Reading file: {filepath}")
    
    try:
        # Check if path is allowed
        if not _is_path_allowed(filepath):
            return {
                "status": "error",
                "error": "Access denied: File path not in allowed directories"
            }
            
        # Check if file exists
        if not os.path.exists(filepath):
            return {
                "status": "error",
                "error": f"File not found: {filepath}"
            }
            
        # Read the file based on extension
        _, ext = os.path.splitext(filepath)
        ext = ext.lower()
        
        if ext in ['.json']:
            # Read as JSON
            with open(filepath, 'r', encoding='utf-8') as f:
                content = json.load(f)
                return {
                    "status": "success",
                    "content": content,
                    "filepath": filepath,
                    "content_type": "json"
                }
                
        elif ext in ['.csv', '.txt', '.md', '.py', '.js', '.html', '.css', '.yml', '.yaml', '.toml']:
            # Read as text
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                return {
                    "status": "success",
                    "content": content,
                    "filepath": filepath,
                    "content_type": "text"
                }
                
        else:
            # For binary files, just return file info
            file_size = os.path.getsize(filepath)
            return {
                "status": "success",
                "content": f"Binary file of size {file_size} bytes",
                "filepath": filepath,
                "content_type": "binary",
                "file_size": file_size
            }
    
    except Exception as e:
        logger.error(f"Error reading file {filepath}: {e}", exc_info=True)
        return {
            "status": "error",
            "error": f"Error reading file: {str(e)}"
        }

def write_file(filepath: str, content: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Write content to a file.
    
    Args:
        filepath: Path to write to (must be in allowed directories)
        content: Content to write to the file (string or JSON-serializable dict)
        
    Returns:
        Dictionary with status and information
    """
    logger.info(f"Writing to file: {filepath}")
    
    try:
        # Check if path is allowed
        if not _is_path_allowed(filepath):
            return {
                "status": "error",
                "error": "Access denied: File path not in allowed directories"
            }
            
        # Create directory if it doesn't exist
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        # Determine file type and write accordingly
        _, ext = os.path.splitext(filepath)
        ext = ext.lower()
        
        if ext == '.json' and isinstance(content, dict):
            # Write as formatted JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2)
                
        elif isinstance(content, str):
            # Write as text
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
        elif isinstance(content, dict):
            # If content is a dict but file isn't .json, serialize to JSON string
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2)
                
        else:
            return {
                "status": "error",
                "error": "Unsupported content type. Must be string or JSON-serializable dict."
            }
            
        return {
            "status": "success",
            "message": f"File written successfully: {filepath}",
            "filepath": filepath
        }
    
    except Exception as e:
        logger.error(f"Error writing to file {filepath}: {e}", exc_info=True)
        return {
            "status": "error",
            "error": f"Error writing to file: {str(e)}"
        }

def list_directory(directory: str) -> Dict[str, Any]:
    """List contents of a directory.
    
    Args:
        directory: Directory path to list (must be in allowed directories)
        
    Returns:
        Dictionary with directory contents or error
    """
    logger.info(f"Listing directory: {directory}")
    
    try:
        # Check if path is allowed
        if not _is_path_allowed(directory):
            return {
                "status": "error",
                "error": "Access denied: Directory path not in allowed directories"
            }
            
        # Check if directory exists
        if not os.path.exists(directory):
            return {
                "status": "error",
                "error": f"Directory not found: {directory}"
            }
            
        if not os.path.isdir(directory):
            return {
                "status": "error",
                "error": f"Not a directory: {directory}"
            }
            
        # List directory contents
        contents = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            item_type = "directory" if os.path.isdir(item_path) else "file"
            
            item_info = {
                "name": item,
                "type": item_type,
                "path": item_path
            }
            
            if item_type == "file":
                item_info["size"] = os.path.getsize(item_path)
                
            contents.append(item_info)
            
        return {
            "status": "success",
            "directory": directory,
            "contents": contents
        }
    
    except Exception as e:
        logger.error(f"Error listing directory {directory}: {e}", exc_info=True)
        return {
            "status": "error",
            "error": f"Error listing directory: {str(e)}"
        } 