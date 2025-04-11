from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.knowledge import (
    KnowledgeBaseCreateRequest,
    KnowledgeBaseCreateResponse,
    KnowledgeBaseListResponse,
    KnowledgeBaseDeleteResponse,
    KnowledgeBaseQueryRequest,
    KnowledgeBaseQueryResponse,
)
from app.services.knowledge import (
    create_knowledge_base,
    list_knowledge_bases,
    delete_knowledge_base,
    query_knowledge_base,
)

router = APIRouter()

@router.post("/create", response_model=KnowledgeBaseCreateResponse)
async def create(request: Request, create_request: KnowledgeBaseCreateRequest):
    """
    Create a new knowledge base
    """
    try:
        kb_id = await create_knowledge_base(
            name=create_request.name,
            description=create_request.description,
            metadata=create_request.metadata,
        )
        return KnowledgeBaseCreateResponse(
            id=kb_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating knowledge base: {str(e)}",
        )

@router.get("/list", response_model=KnowledgeBaseListResponse)
async def list_kbs(request: Request):
    """
    List all knowledge bases
    """
    try:
        knowledge_bases = await list_knowledge_bases()
        return KnowledgeBaseListResponse(
            knowledge_bases=knowledge_bases,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing knowledge bases: {str(e)}",
        )

@router.delete("/{kb_id}", response_model=KnowledgeBaseDeleteResponse)
async def delete(request: Request, kb_id: str):
    """
    Delete a knowledge base
    """
    try:
        success = await delete_knowledge_base(kb_id)
        return KnowledgeBaseDeleteResponse(
            success=success,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting knowledge base: {str(e)}",
        )

@router.post("/query", response_model=KnowledgeBaseQueryResponse)
async def query(request: Request, query_request: KnowledgeBaseQueryRequest):
    """
    Query a knowledge base
    """
    try:
        results = await query_knowledge_base(
            kb_id=query_request.kb_id,
            query=query_request.query,
            k=query_request.k,
            filter=query_request.filter,
        )
        return KnowledgeBaseQueryResponse(
            results=results,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error querying knowledge base: {str(e)}",
        )
