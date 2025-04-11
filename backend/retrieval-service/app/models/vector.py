from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class VectorSearchRequest(BaseModel):
    """Vector search request"""
    collection_name: str
    query: str
    k: int = 5
    filter: Optional[Dict[str, Any]] = None


class VectorSearchResult(BaseModel):
    """Vector search result"""
    id: str
    text: str
    metadata: Dict[str, Any]
    score: float


class VectorSearchResponse(BaseModel):
    """Vector search response"""
    results: List[VectorSearchResult]


class VectorUpsertRequest(BaseModel):
    """Vector upsert request"""
    collection_name: str
    texts: List[str]
    metadatas: Optional[List[Dict[str, Any]]] = None
    ids: Optional[List[str]] = None


class VectorUpsertResponse(BaseModel):
    """Vector upsert response"""
    ids: List[str]


class VectorDeleteRequest(BaseModel):
    """Vector delete request"""
    collection_name: str
    ids: Optional[List[str]] = None
    filter: Optional[Dict[str, Any]] = None


class VectorDeleteResponse(BaseModel):
    """Vector delete response"""
    success: bool
