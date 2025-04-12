import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from common.db.async_base import Base, JSONField


# Association table for chat-tag many-to-many relationship
chat_tags = Table(
    "chat_tags",
    Base.metadata,
    Column("chat_id", String, ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", String, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)


class Chat(Base):
    """Chat model for database"""
    __tablename__ = "chats"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    system = Column(String, nullable=True)
    models = Column(JSONField, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    share_id = Column(String, nullable=True, unique=True, index=True)
    archived = Column(Boolean, default=False)
    pinned = Column(Boolean, default=False)
    folder_id = Column(String, ForeignKey("folders.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    folder = relationship("Folder", back_populates="chats")
    tags = relationship("Tag", secondary=chat_tags, back_populates="chats")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "system": self.system,
            "models": self.models,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "share_id": self.share_id,
            "archived": self.archived,
            "pinned": self.pinned,
            "folder_id": self.folder_id,
            "tags": [tag.id for tag in self.tags] if self.tags else []
        }


class Message(Base):
    """Message model for database"""
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    chat_id = Column(String, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(String, nullable=False)
    role = Column(String, nullable=False)
    parent_id = Column(String, ForeignKey("messages.id", ondelete="SET NULL"), nullable=True)
    model = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    meta_data = Column(JSONField, nullable=True)  # renamed from metadata to avoid conflict with SQLAlchemy

    # Relationships
    chat = relationship("Chat", back_populates="messages")
    parent = relationship("Message", remote_side=[id], backref="children")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "chat_id": self.chat_id,
            "content": self.content,
            "role": self.role,
            "parent_id": self.parent_id,
            "model": self.model,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.meta_data,
            "children_ids": [child.id for child in self.children] if self.children else []
        }


class Folder(Base):
    """Folder model for database"""
    __tablename__ = "folders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    chats = relationship("Chat", back_populates="folder")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "chat_count": len(self.chats) if self.chats else 0
        }


class Tag(Base):
    """Tag model for database"""
    __tablename__ = "tags"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False, default="#808080")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    chats = relationship("Chat", secondary=chat_tags, back_populates="tags")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "color": self.color,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "chat_count": len(self.chats) if self.chats else 0
        }
