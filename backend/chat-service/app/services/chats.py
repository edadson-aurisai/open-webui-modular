import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.chats import ChatResponse, ChatListItem
from app.db.models import Chat, Message, Tag
from common.db.async_base import get_async_db

logger = logging.getLogger(__name__)


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
        async with get_async_db() as db:
            # Create the chat
            chat = Chat(
                user_id=user_id,
                title=title,
                models=models,
                system=system,
            )

            # Add tags if provided
            if tags:
                # Get existing tags
                stmt = select(Tag).where(Tag.id.in_(tags), Tag.user_id == user_id)
                result = await db.execute(stmt)
                existing_tags = result.scalars().all()
                chat.tags = existing_tags

            # Add to database
            db.add(chat)
            await db.commit()
            await db.refresh(chat)

            # Create messages if provided
            if messages:
                for msg in messages:
                    message = Message(
                        user_id=user_id,
                        chat_id=chat.id,
                        content=msg.get("content", ""),
                        role=msg.get("role", "user"),
                        parent_id=msg.get("parent_id"),
                        model=msg.get("model"),
                        metadata=msg.get("metadata", {}),
                    )
                    db.add(message)

                await db.commit()

            return chat.id
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
        async with get_async_db() as db:
            # Get the chat
            stmt = select(Chat).where(Chat.id == chat_id, Chat.user_id == user_id)
            result = await db.execute(stmt)
            chat = result.scalars().first()

            if not chat:
                return None

            # Update chat properties
            chat.title = title
            chat.models = models
            chat.system = system
            chat.updated_at = datetime.now()

            # Update tags if provided
            if tags is not None:
                # Get existing tags
                stmt = select(Tag).where(Tag.id.in_(tags), Tag.user_id == user_id)
                result = await db.execute(stmt)
                existing_tags = result.scalars().all()
                chat.tags = existing_tags

            # Update messages if provided
            if messages:
                # Delete existing messages
                stmt = delete(Message).where(Message.chat_id == chat_id)
                await db.execute(stmt)

                # Create new messages
                for msg in messages:
                    message = Message(
                        user_id=user_id,
                        chat_id=chat.id,
                        content=msg.get("content", ""),
                        role=msg.get("role", "user"),
                        parent_id=msg.get("parent_id"),
                        model=msg.get("model"),
                        metadata=msg.get("metadata", {}),
                    )
                    db.add(message)

            await db.commit()
            await db.refresh(chat)

            # Convert to response model
            return ChatResponse(
                id=chat.id,
                user_id=chat.user_id,
                title=chat.title,
                models=chat.models,
                system=chat.system,
                messages=[msg.to_dict() for msg in chat.messages],
                created_at=chat.created_at,
                updated_at=chat.updated_at,
                share_id=chat.share_id,
                archived=chat.archived,
                pinned=chat.pinned,
                folder_id=chat.folder_id,
                tags=[tag.id for tag in chat.tags] if chat.tags else [],
            )
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
        async with get_async_db() as db:
            # Get the chat with messages and tags
            stmt = select(Chat).where(
                Chat.id == chat_id,
                Chat.user_id == user_id
            ).options(
                selectinload(Chat.messages),
                selectinload(Chat.tags)
            )
            result = await db.execute(stmt)
            chat = result.scalars().first()

            if not chat:
                return None

            # Convert to response model
            return ChatResponse(
                id=chat.id,
                user_id=chat.user_id,
                title=chat.title,
                models=chat.models,
                system=chat.system,
                messages=[msg.to_dict() for msg in chat.messages],
                created_at=chat.created_at,
                updated_at=chat.updated_at,
                share_id=chat.share_id,
                archived=chat.archived,
                pinned=chat.pinned,
                folder_id=chat.folder_id,
                tags=[tag.id for tag in chat.tags] if chat.tags else [],
            )
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
        async with get_async_db() as db:
            # Calculate offset
            offset = (page - 1) * limit

            # Get chats with tags
            stmt = select(Chat).where(
                Chat.user_id == user_id,
                Chat.archived == False
            ).options(
                selectinload(Chat.tags)
            ).order_by(
                Chat.updated_at.desc()
            ).offset(offset).limit(limit)

            result = await db.execute(stmt)
            chats = result.scalars().all()

            # Convert to response model
            return [
                ChatListItem(
                    id=chat.id,
                    title=chat.title,
                    updated_at=chat.updated_at,
                    created_at=chat.created_at,
                    pinned=chat.pinned,
                    folder_id=chat.folder_id,
                    tags=[tag.id for tag in chat.tags] if chat.tags else [],
                )
                for chat in chats
            ]
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
        async with get_async_db() as db:
            # Get the chat
            stmt = select(Chat).where(Chat.id == chat_id, Chat.user_id == user_id)
            result = await db.execute(stmt)
            chat = result.scalars().first()

            if not chat:
                return False

            # Delete the chat (cascade will delete messages and chat_tags)
            await db.delete(chat)
            await db.commit()

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
        async with get_async_db() as db:
            # Get the chat
            stmt = select(Chat).where(Chat.id == chat_id, Chat.user_id == user_id)
            result = await db.execute(stmt)
            chat = result.scalars().first()

            if not chat:
                return None

            # Generate a share ID if not already shared
            if not chat.share_id:
                chat.share_id = str(uuid.uuid4())
                await db.commit()

            return chat.share_id
    except Exception as e:
        logger.error(f"Error sharing chat: {e}")
        raise
