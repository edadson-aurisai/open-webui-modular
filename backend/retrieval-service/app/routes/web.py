from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.web import (
    WebSearchRequest,
    WebSearchResponse,
    WebFetchRequest,
    WebFetchResponse,
)
from app.services.web import (
    search_web,
    fetch_web_content,
)

router = APIRouter()

@router.post("/search", response_model=WebSearchResponse)
async def search(request: Request, search_request: WebSearchRequest):
    """
    Search the web using the configured search engine
    """
    if not settings.enable_rag_web_search:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Web search is disabled",
        )
    
    try:
        results = await search_web(
            query=search_request.query,
            engine=search_request.engine or settings.rag_web_search_engine,
            count=search_request.count or settings.rag_web_search_result_count,
        )
        return WebSearchResponse(
            results=results,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching web: {str(e)}",
        )

@router.post("/fetch", response_model=WebFetchResponse)
async def fetch(request: Request, fetch_request: WebFetchRequest):
    """
    Fetch content from a web URL
    """
    if not settings.enable_rag_local_web_fetch:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Web fetch is disabled",
        )
    
    try:
        content = await fetch_web_content(
            url=fetch_request.url,
        )
        return WebFetchResponse(
            content=content,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching web content: {str(e)}",
        )
