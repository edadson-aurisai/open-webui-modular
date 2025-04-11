import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.core.config import settings
from app.models.tags import TagResponse

logger = logging.getLogger(__name__)

# In-memory database of tags (would be replaced with a real database in production)
tags_db = {}


async def create_tag(
    user_id: str,
    name: str,
    color: Optional[str] = None,
) -> str:
    """
    Create a new tag
    """
    try:
        # Generate a tag ID
        tag_id = str(uuid.uuid4())
        
        # Create the tag
        now = datetime.now()
        tags_db[tag_id] = {
            "id": tag_id,
            "user_id": user_id,
            "name": name,
            "color": color or "#808080",  # Default to gray if no color provided
            "created_at": now,
            "updated_at": now,
            "chat_count": 0,
        }
        
        return tag_id
    except Exception as e:
        logger.error(f"Error creating tag: {e}")
        raise


async def update_tag(
    tag_id: str,
    user_id: str,
    name: str,
    color: Optional[str] = None,
) -> Optional[TagResponse]:
    """
    Update a tag
    """
    try:
        # Check if the tag exists and belongs to the user
        if tag_id not in tags_db or tags_db[tag_id]["user_id"] != user_id:
            return None
        
        # Update the tag
        tags_db[tag_id].update({
            "name": name,
            "color": color or tags_db[tag_id]["color"],
            "updated_at": datetime.now(),
        })
        
        return TagResponse(**tags_db[tag_id])
    except Exception as e:
        logger.error(f"Error updating tag: {e}")
        raise


async def get_tag(
    tag_id: str,
    user_id: str,
) -> Optional[TagResponse]:
    """
    Get a tag by ID
    """
    try:
        # Check if the tag exists and belongs to the user
        if tag_id not in tags_db or tags_db[tag_id]["user_id"] != user_id:
            return None
        
        return TagResponse(**tags_db[tag_id])
    except Exception as e:
        logger.error(f"Error getting tag: {e}")
        raise


async def list_tags(
    user_id: str,
) -> List[TagResponse]:
    """
    List all tags for a user
    """
    try:
        # Filter tags by user ID
        user_tags = [
            TagResponse(**tag)
            for tag_id, tag in tags_db.items()
            if tag["user_id"] == user_id
        ]
        
        # Sort by name
        user_tags.sort(key=lambda x: x.name)
        
        return user_tags
    except Exception as e:
        logger.error(f"Error listing tags: {e}")
        raise


async def delete_tag(
    tag_id: str,
    user_id: str,
) -> bool:
    """
    Delete a tag
    """
    try:
        # Check if the tag exists and belongs to the user
        if tag_id not in tags_db or tags_db[tag_id]["user_id"] != user_id:
            return False
        
        # Delete the tag
        del tags_db[tag_id]
        
        return True
    except Exception as e:
        logger.error(f"Error deleting tag: {e}")
        raise
