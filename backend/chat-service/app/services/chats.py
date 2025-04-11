import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.core.config import settings
from app.models.chats import ChatResponse, ChatListItem

logger = logging.getLogger(__name__)

# In-memory database of chats (would be replaced with a real database in production)
chats_db = {}


async def create_chat(
    user_id: str,
    title: str,
    messages: List[Dict[str, Any]],
    models: List[Dict[str, Any]],
    system: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> str:
    """
    Create a new chat
    """
    try:
        # Generate a chat ID
        chat_id = str(uuid.uuid4())
        
        # Create the chat
        now = datetime.now()
        chats_db[chat_id] = {
            "id": chat_id,
            "user_id": user_id,
            "title": title,
            "messages": messages,
            "models": models,
            "system": system,
            "tags": tags or [],
            "created_at": now,
            "updated_at": now,
            "share_id": None,
            "archived": False,
            "pinned": False,
            "folder_id": None,
        }
        
        return chat_id
    except Exception as e:
        logger.error(f"Error creating chat: {e}")
        raise


async def update_chat(
    chat_id: str,
    user_id: str,
    title: str,
    messages: List[Dict[str, Any]],
    models: List[Dict[str, Any]],
    system: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> Optional[ChatResponse]:
    """
    Update a chat
    """
    try:
        # Check if the chat exists and belongs to the user
        if chat_id not in chats_db or chats_db[chat_id]["user_id"] != user_id:
            return None
        
        # Update the chat
        chats_db[chat_id].update({
            "title": title,
            "messages": messages,
            "models": models,
            "system": system,
            "tags": tags or chats_db[chat_id]["tags"],
            "updated_at": datetime.now(),
        })
        
        return ChatResponse(**chats_db[chat_id])
    except Exception as e:
        logger.error(f"Error updating chat: {e}")
        raise


async def get_chat(
    chat_id: str,
    user_id: str,
) -> Optional[ChatResponse]:
    """
    Get a chat by ID
    """
    try:
        # Check if the chat exists and belongs to the user
        if chat_id not in chats_db or chats_db[chat_id]["user_id"] != user_id:
            return None
        
        return ChatResponse(**chats_db[chat_id])
    except Exception as e:
        logger.error(f"Error getting chat: {e}")
        raise


async def list_chats(
    user_id: str,
    page: int = 1,
    limit: int = 50,
) -> List[ChatListItem]:
    """
    List all chats for a user
    """
    try:
        # Filter chats by user ID
        user_chats = [
            ChatListItem(
                id=chat_id,
                title=chat["title"],
                updated_at=chat["updated_at"],
                created_at=chat["created_at"],
                pinned=chat["pinned"],
                folder_id=chat["folder_id"],
                tags=chat["tags"],
            )
            for chat_id, chat in chats_db.items()
            if chat["user_id"] == user_id and not chat["archived"]
        ]
        
        # Sort by updated_at (newest first)
        user_chats.sort(key=lambda x: x.updated_at, reverse=True)
        
        # Paginate
        start = (page - 1) * limit
        end = start + limit
        
        return user_chats[start:end]
    except Exception as e:
        logger.error(f"Error listing chats: {e}")
        raise


async def delete_chat(
    chat_id: str,
    user_id: str,
) -> bool:
    """
    Delete a chat
    """
    try:
        # Check if the chat exists and belongs to the user
        if chat_id not in chats_db or chats_db[chat_id]["user_id"] != user_id:
            return False
        
        # Delete the chat
        del chats_db[chat_id]
        
        return True
    except Exception as e:
        logger.error(f"Error deleting chat: {e}")
        raise


async def share_chat(
    chat_id: str,
    user_id: str,
) -> Optional[str]:
    """
    Share a chat
    """
    try:
        # Check if the chat exists and belongs to the user
        if chat_id not in chats_db or chats_db[chat_id]["user_id"] != user_id:
            return None
        
        # Generate a share ID if not already shared
        if not chats_db[chat_id]["share_id"]:
            chats_db[chat_id]["share_id"] = str(uuid.uuid4())
        
        return chats_db[chat_id]["share_id"]
    except Exception as e:
        logger.error(f"Error sharing chat: {e}")
        raise
