from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class TagBase(BaseModel):
    """Base tag model"""
    name: str
    color: Optional[str] = None


class TagCreateRequest(TagBase):
    """Tag creation request"""
    pass


class TagCreateResponse(BaseModel):
    """Tag creation response"""
    id: str


class TagUpdateRequest(TagBase):
    """Tag update request"""
    pass


class TagResponse(TagBase):
    """Tag response"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    chat_count: int = 0


class TagListResponse(BaseModel):
    """Tag list response"""
    tags: List[TagResponse]
