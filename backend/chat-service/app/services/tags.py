import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.tags import TagResponse
from app.db.models import Tag, Chat, chat_tags
from common.db.async_base import get_async_db

logger = logging.getLogger(__name__)


async def create_tag(
    user_id: str,
    name: str,
    color: Optional[str] = None,
) -> str:
    """
    Create a new tag
    """
    try:
        async with get_async_db() as db:
            # Create the tag
            tag = Tag(
                user_id=user_id,
                name=name,
                color=color or "#808080",  # Default to gray if no color provided
            )

            # Add to database
            db.add(tag)
            await db.commit()
            await db.refresh(tag)

            return str(tag.id)
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
        async with get_async_db() as db:
            # Get the tag
            stmt = select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
            result = await db.execute(stmt)
            tag = result.scalars().first()

            if not tag:
                return None

            # Update tag properties
            tag.name = name
            if color:
                tag.color = color
            tag.updated_at = datetime.now()

            await db.commit()
            await db.refresh(tag)

            # Get chat count
            stmt = select(func.count()).select_from(chat_tags).where(chat_tags.c.tag_id == tag_id)
            result = await db.execute(stmt)
            chat_count = result.scalar() or 0

            # Convert to response model
            return TagResponse(
                id=str(tag.id),
                user_id=str(tag.user_id),
                name=str(tag.name),
                color=str(tag.color),
                created_at=tag.created_at,
                updated_at=tag.updated_at,
                chat_count=chat_count,
            )
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
        async with get_async_db() as db:
            # Get the tag
            stmt = select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
            result = await db.execute(stmt)
            tag = result.scalars().first()

            if not tag:
                return None

            # Get chat count
            stmt = select(func.count()).select_from(chat_tags).where(chat_tags.c.tag_id == tag_id)
            result = await db.execute(stmt)
            chat_count = result.scalar() or 0

            # Convert to response model
            return TagResponse(
                id=str(tag.id),
                user_id=str(tag.user_id),
                name=str(tag.name),
                color=str(tag.color),
                created_at=tag.created_at,
                updated_at=tag.updated_at,
                chat_count=chat_count,
            )
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
        async with get_async_db() as db:
            # Get tags
            stmt = select(Tag).where(Tag.user_id == user_id).order_by(Tag.name)
            result = await db.execute(stmt)
            tags = result.scalars().all()

            # Get chat counts for each tag
            tag_responses = []
            for tag in tags:
                # Get chat count
                stmt = select(func.count()).select_from(chat_tags).where(chat_tags.c.tag_id == tag.id)
                result = await db.execute(stmt)
                chat_count = result.scalar() or 0

                # Convert to response model
                tag_responses.append(TagResponse(
                    id=str(tag.id),
                    user_id=str(tag.user_id),
                    name=str(tag.name),
                    color=str(tag.color),
                    created_at=tag.created_at,
                    updated_at=tag.updated_at,
                    chat_count=chat_count,
                ))

            return tag_responses
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
        async with get_async_db() as db:
            # Get the tag
            stmt = select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
            result = await db.execute(stmt)
            tag = result.scalars().first()

            if not tag:
                return False

            # Delete the tag (association table entries will be deleted automatically)
            await db.delete(tag)
            await db.commit()

            return True
    except Exception as e:
        logger.error(f"Error deleting tag: {e}")
        raise
