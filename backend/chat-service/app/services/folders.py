import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.folders import FolderResponse
from app.db.models import Folder, Chat
from common.db.async_base import get_async_db

logger = logging.getLogger(__name__)


async def create_folder(
    user_id: str,
    name: str,
    description: Optional[str] = None,
) -> str:
    """
    Create a new folder
    """
    try:
        async with get_async_db() as db:
            # Create the folder
            folder = Folder(
                user_id=user_id,
                name=name,
                description=description,
            )

            # Add to database
            db.add(folder)
            await db.commit()
            await db.refresh(folder)

            return str(folder.id)
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
        async with get_async_db() as db:
            # Get the folder
            stmt = select(Folder).where(Folder.id == folder_id, Folder.user_id == user_id)
            result = await db.execute(stmt)
            folder = result.scalars().first()

            if not folder:
                return None

            # Update folder properties
            folder.name = name
            folder.description = description
            folder.updated_at = datetime.now()

            await db.commit()
            await db.refresh(folder)

            # Get chat count
            stmt = select(Chat).where(Chat.folder_id == folder_id)
            result = await db.execute(stmt)
            chat_count = len(result.scalars().all())

            # Convert to response model
            return FolderResponse(
                id=str(folder.id),
                user_id=str(folder.user_id),
                name=str(folder.name),
                description=str(folder.description) if folder.description else None,
                created_at=folder.created_at,
                updated_at=folder.updated_at,
                chat_count=chat_count,
            )
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
        async with get_async_db() as db:
            # Get the folder
            stmt = select(Folder).where(Folder.id == folder_id, Folder.user_id == user_id)
            result = await db.execute(stmt)
            folder = result.scalars().first()

            if not folder:
                return None

            # Get chat count
            stmt = select(Chat).where(Chat.folder_id == folder_id)
            result = await db.execute(stmt)
            chat_count = len(result.scalars().all())

            # Convert to response model
            return FolderResponse(
                id=str(folder.id),
                user_id=str(folder.user_id),
                name=str(folder.name),
                description=str(folder.description) if folder.description else None,
                created_at=folder.created_at,
                updated_at=folder.updated_at,
                chat_count=chat_count,
            )
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
        async with get_async_db() as db:
            # Get folders
            stmt = select(Folder).where(Folder.user_id == user_id).order_by(Folder.name)
            result = await db.execute(stmt)
            folders = result.scalars().all()

            # Get chat counts for each folder
            folder_responses = []
            for folder in folders:
                # Get chat count
                stmt = select(Chat).where(Chat.folder_id == folder.id)
                result = await db.execute(stmt)
                chat_count = len(result.scalars().all())

                # Convert to response model
                folder_responses.append(FolderResponse(
                    id=str(folder.id),
                    user_id=str(folder.user_id),
                    name=str(folder.name),
                    description=str(folder.description) if folder.description else None,
                    created_at=folder.created_at,
                    updated_at=folder.updated_at,
                    chat_count=chat_count,
                ))

            return folder_responses
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
        async with get_async_db() as db:
            # Get the folder
            stmt = select(Folder).where(Folder.id == folder_id, Folder.user_id == user_id)
            result = await db.execute(stmt)
            folder = result.scalars().first()

            if not folder:
                return False

            # Update chats to remove folder_id
            stmt = select(Chat).where(Chat.folder_id == folder_id)
            result = await db.execute(stmt)
            chats = result.scalars().all()

            for chat in chats:
                chat.folder_id = None

            # Delete the folder
            await db.delete(folder)
            await db.commit()

            return True
    except Exception as e:
        logger.error(f"Error deleting folder: {e}")
        raise
