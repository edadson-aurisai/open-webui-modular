from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class FileInfo(BaseModel):
    """File information"""
    id: str
    filename: str
    collection_name: str
    document_count: int
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None


class FileUploadResponse(BaseModel):
    """File upload response"""
    id: str
    filename: str
    document_ids: List[str]


class FileListResponse(BaseModel):
    """File list response"""
    files: List[FileInfo]


class FileDeleteResponse(BaseModel):
    """File delete response"""
    success: bool
