from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class WebSearchRequest(BaseModel):
    """Web search request"""
    query: str
    engine: Optional[str] = None
    count: Optional[int] = None


class WebSearchResult(BaseModel):
    """Web search result"""
    title: str
    url: str
    snippet: str


class WebSearchResponse(BaseModel):
    """Web search response"""
    results: List[WebSearchResult]


class WebFetchRequest(BaseModel):
    """Web fetch request"""
    url: str


class WebFetchResponse(BaseModel):
    """Web fetch response"""
    content: str
