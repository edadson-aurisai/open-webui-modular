import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.messages import MessageResponse
from app.db.models import Message, Chat
from common.db.async_base import get_async_db

logger = logging.getLogger(__name__)


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
        async with get_async_db() as db:
            # Verify chat exists and belongs to user
            stmt = select(Chat).where(Chat.id == chat_id, Chat.user_id == user_id)
            result = await db.execute(stmt)
            chat = result.scalars().first()

            if not chat:
                raise ValueError(f"Chat {chat_id} not found or does not belong to user {user_id}")

            # Create the message
            message = Message(
                user_id=user_id,
                chat_id=chat_id,
                content=content,
                role=role,
                parent_id=parent_id,
                model=model,
                meta_data={},
            )

            db.add(message)
            await db.commit()
            await db.refresh(message)

            return message.id
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
        async with get_async_db() as db:
            # Get the message with children
            stmt = select(Message).where(
                Message.id == message_id,
                Message.user_id == user_id
            ).options(
                selectinload(Message.children)
            )
            result = await db.execute(stmt)
            message = result.scalars().first()

            if not message:
                return None

            # Convert to response model
            return MessageResponse(
                id=message.id,
                user_id=message.user_id,
                chat_id=message.chat_id,
                content=message.content,
                role=message.role,
                parent_id=message.parent_id,
                model=message.model,
                created_at=message.created_at,
                updated_at=message.updated_at,
                children_ids=[child.id for child in message.children] if message.children else [],
                metadata=message.meta_data or {},
            )
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
        async with get_async_db() as db:
            # Verify chat exists and belongs to user
            stmt = select(Chat).where(Chat.id == chat_id, Chat.user_id == user_id)
            result = await db.execute(stmt)
            chat = result.scalars().first()

            if not chat:
                return []

            # Get all messages for the chat
            stmt = select(Message).where(
                Message.chat_id == chat_id,
                Message.user_id == user_id
            ).options(
                selectinload(Message.children)
            ).order_by(Message.created_at)

            result = await db.execute(stmt)
            messages = result.scalars().all()

            # Convert to response model
            return [
                MessageResponse(
                    id=msg.id,
                    user_id=msg.user_id,
                    chat_id=msg.chat_id,
                    content=msg.content,
                    role=msg.role,
                    parent_id=msg.parent_id,
                    model=msg.model,
                    created_at=msg.created_at,
                    updated_at=msg.updated_at,
                    children_ids=[child.id for child in msg.children] if msg.children else [],
                    metadata=msg.meta_data or {},
                )
                for msg in messages
            ]
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
        async with get_async_db() as db:
            # Get the message
            stmt = select(Message).where(Message.id == message_id, Message.user_id == user_id)
            result = await db.execute(stmt)
            message = result.scalars().first()

            if not message:
                return False

            # Delete the message (SQLAlchemy will handle parent/child relationships)
            await db.delete(message)
            await db.commit()

            return True
    except Exception as e:
        logger.error(f"Error deleting message: {e}")
        raise
