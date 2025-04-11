import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.core.config import settings
from app.models.folders import FolderResponse

logger = logging.getLogger(__name__)

# In-memory database of folders (would be replaced with a real database in production)
folders_db = {}


async def create_folder(
    user_id: str,
    name: str,
    description: Optional[str] = None,
) -> str:
    """
    Create a new folder
    """
    try:
        # Generate a folder ID
        folder_id = str(uuid.uuid4())
        
        # Create the folder
        now = datetime.now()
        folders_db[folder_id] = {
            "id": folder_id,
            "user_id": user_id,
            "name": name,
            "description": description,
            "created_at": now,
            "updated_at": now,
            "chat_count": 0,
        }
        
        return folder_id
    except Exception as e:
        logger.error(f"Error creating folder: {e}")
        raise


async def update_folder(
    folder_id: str,
    user_id: str,
    name: str,
    description: Optional[str] = None,
) -> Optional[FolderResponse]:
    """
    Update a folder
    """
    try:
        # Check if the folder exists and belongs to the user
        if folder_id not in folders_db or folders_db[folder_id]["user_id"] != user_id:
            return None
        
        # Update the folder
        folders_db[folder_id].update({
            "name": name,
            "description": description,
            "updated_at": datetime.now(),
        })
        
        return FolderResponse(**folders_db[folder_id])
    except Exception as e:
        logger.error(f"Error updating folder: {e}")
        raise


async def get_folder(
    folder_id: str,
    user_id: str,
) -> Optional[FolderResponse]:
    """
    Get a folder by ID
    """
    try:
        # Check if the folder exists and belongs to the user
        if folder_id not in folders_db or folders_db[folder_id]["user_id"] != user_id:
            return None
        
        return FolderResponse(**folders_db[folder_id])
    except Exception as e:
        logger.error(f"Error getting folder: {e}")
        raise


async def list_folders(
    user_id: str,
) -> List[FolderResponse]:
    """
    List all folders for a user
    """
    try:
        # Filter folders by user ID
        user_folders = [
            FolderResponse(**folder)
            for folder_id, folder in folders_db.items()
            if folder["user_id"] == user_id
        ]
        
        # Sort by name
        user_folders.sort(key=lambda x: x.name)
        
        return user_folders
    except Exception as e:
        logger.error(f"Error listing folders: {e}")
        raise


async def delete_folder(
    folder_id: str,
    user_id: str,
) -> bool:
    """
    Delete a folder
    """
    try:
        # Check if the folder exists and belongs to the user
        if folder_id not in folders_db or folders_db[folder_id]["user_id"] != user_id:
            return False
        
        # Delete the folder
        del folders_db[folder_id]
        
        return True
    except Exception as e:
        logger.error(f"Error deleting folder: {e}")
        raise
