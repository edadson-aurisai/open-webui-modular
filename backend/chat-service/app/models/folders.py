from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class FolderBase(BaseModel):
    """Base folder model"""
    name: str
    description: Optional[str] = None


class FolderCreateRequest(FolderBase):
    """Folder creation request"""
    pass


class FolderCreateResponse(BaseModel):
    """Folder creation response"""
    id: str


class FolderUpdateRequest(FolderBase):
    """Folder update request"""
    pass


class FolderResponse(FolderBase):
    """Folder response"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    chat_count: int = 0


class FolderListResponse(BaseModel):
    """Folder list response"""
    folders: List[FolderResponse]
