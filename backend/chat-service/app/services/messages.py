import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.core.config import settings
from app.models.messages import MessageResponse

logger = logging.getLogger(__name__)

# In-memory database of messages (would be replaced with a real database in production)
messages_db = {}


async def create_message(
    user_id: str,
    chat_id: str,
    content: str,
    role: str,
    parent_id: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    """
    Create a new message
    """
    try:
        # Generate a message ID
        message_id = str(uuid.uuid4())
        
        # Create the message
        now = datetime.now()
        messages_db[message_id] = {
            "id": message_id,
            "user_id": user_id,
            "chat_id": chat_id,
            "content": content,
            "role": role,
            "parent_id": parent_id,
            "model": model,
            "created_at": now,
            "updated_at": now,
            "children_ids": [],
            "metadata": {},
        }
        
        # Update parent message if it exists
        if parent_id and parent_id in messages_db:
            messages_db[parent_id]["children_ids"].append(message_id)
        
        return message_id
    except Exception as e:
        logger.error(f"Error creating message: {e}")
        raise


async def get_message(
    message_id: str,
    user_id: str,
) -> Optional[MessageResponse]:
    """
    Get a message by ID
    """
    try:
        # Check if the message exists and belongs to the user
        if message_id not in messages_db or messages_db[message_id]["user_id"] != user_id:
            return None
        
        return MessageResponse(**messages_db[message_id])
    except Exception as e:
        logger.error(f"Error getting message: {e}")
        raise


async def list_messages(
    chat_id: str,
    user_id: str,
) -> List[MessageResponse]:
    """
    List all messages for a chat
    """
    try:
        # Filter messages by chat ID and user ID
        chat_messages = [
            MessageResponse(**message)
            for message_id, message in messages_db.items()
            if message["chat_id"] == chat_id and message["user_id"] == user_id
        ]
        
        # Sort by created_at (oldest first)
        chat_messages.sort(key=lambda x: x.created_at)
        
        return chat_messages
    except Exception as e:
        logger.error(f"Error listing messages: {e}")
        raise


async def delete_message(
    message_id: str,
    user_id: str,
) -> bool:
    """
    Delete a message
    """
    try:
        # Check if the message exists and belongs to the user
        if message_id not in messages_db or messages_db[message_id]["user_id"] != user_id:
            return False
        
        # Remove from parent's children_ids if it has a parent
        parent_id = messages_db[message_id]["parent_id"]
        if parent_id and parent_id in messages_db:
            messages_db[parent_id]["children_ids"].remove(message_id)
        
        # Delete the message
        del messages_db[message_id]
        
        return True
    except Exception as e:
        logger.error(f"Error deleting message: {e}")
        raise
