from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class MessageBase(BaseModel):
    """Base message model"""
    content: str
    role: str
    chat_id: str
    parent_id: Optional[str] = None
    model: Optional[str] = None


class MessageCreateRequest(MessageBase):
    """Message creation request"""
    pass


class MessageCreateResponse(BaseModel):
    """Message creation response"""
    id: str


class MessageResponse(MessageBase):
    """Message response"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    children_ids: List[str] = []
    metadata: Optional[Dict[str, Any]] = None


class MessageListResponse(BaseModel):
    """Message list response"""
    messages: List[MessageResponse]
