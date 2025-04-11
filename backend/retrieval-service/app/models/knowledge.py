from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class KnowledgeBase(BaseModel):
    """Knowledge base"""
    id: str
    name: str
    description: Optional[str] = None
    document_count: int
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None


class KnowledgeBaseCreateRequest(BaseModel):
    """Knowledge base create request"""
    name: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class KnowledgeBaseCreateResponse(BaseModel):
    """Knowledge base create response"""
    id: str


class KnowledgeBaseListResponse(BaseModel):
    """Knowledge base list response"""
    knowledge_bases: List[KnowledgeBase]


class KnowledgeBaseDeleteResponse(BaseModel):
    """Knowledge base delete response"""
    success: bool


class KnowledgeBaseQueryRequest(BaseModel):
    """Knowledge base query request"""
    kb_id: str
    query: str
    k: int = 5
    filter: Optional[Dict[str, Any]] = None


class KnowledgeBaseQueryResult(BaseModel):
    """Knowledge base query result"""
    id: str
    text: str
    metadata: Dict[str, Any]
    score: float


class KnowledgeBaseQueryResponse(BaseModel):
    """Knowledge base query response"""
    results: List[KnowledgeBaseQueryResult]
