from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class ChatBase(BaseModel):
    """Base chat model"""
    title: str
    models: List[Dict[str, Any]]
    system: Optional[str] = None
    tags: Optional[List[str]] = None


class ChatCreateRequest(ChatBase):
    """Chat creation request"""
    messages: List[Dict[str, Any]] = []


class ChatCreateResponse(BaseModel):
    """Chat creation response"""
    id: str


class ChatUpdateRequest(ChatBase):
    """Chat update request"""
    messages: List[Dict[str, Any]] = []


class ChatResponse(ChatBase):
    """Chat response"""
    id: str
    user_id: str
    messages: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    share_id: Optional[str] = None
    archived: bool = False
    pinned: bool = False
    folder_id: Optional[str] = None


class ChatListItem(BaseModel):
    """Chat list item"""
    id: str
    title: str
    updated_at: datetime
    created_at: datetime
    pinned: bool = False
    folder_id: Optional[str] = None
    tags: Optional[List[str]] = None


class ChatListResponse(BaseModel):
    """Chat list response"""
    chats: List[ChatListItem]
