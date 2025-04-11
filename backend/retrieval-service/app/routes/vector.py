from fastapi import APIRouter, Depends, HTTPException, Request, status, UploadFile, File
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.vector import (
    VectorSearchRequest,
    VectorSearchResponse,
    VectorUpsertRequest,
    VectorUpsertResponse,
    VectorDeleteRequest,
    VectorDeleteResponse,
)
from app.services.vector import (
    search_vectors,
    upsert_vectors,
    delete_vectors,
    get_embedding,
)

router = APIRouter()

@router.post("/search", response_model=VectorSearchResponse)
async def search(request: Request, search_request: VectorSearchRequest):
    """
    Search for vectors in the vector database
    """
    try:
        results = await search_vectors(
            collection_name=search_request.collection_name,
            query=search_request.query,
            k=search_request.k,
            filter=search_request.filter,
        )
        return VectorSearchResponse(
            results=results,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching vectors: {str(e)}",
        )

@router.post("/upsert", response_model=VectorUpsertResponse)
async def upsert(request: Request, upsert_request: VectorUpsertRequest):
    """
    Upsert vectors into the vector database
    """
    try:
        ids = await upsert_vectors(
            collection_name=upsert_request.collection_name,
            texts=upsert_request.texts,
            metadatas=upsert_request.metadatas,
            ids=upsert_request.ids,
        )
        return VectorUpsertResponse(
            ids=ids,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error upserting vectors: {str(e)}",
        )

@router.post("/delete", response_model=VectorDeleteResponse)
async def delete(request: Request, delete_request: VectorDeleteRequest):
    """
    Delete vectors from the vector database
    """
    try:
        success = await delete_vectors(
            collection_name=delete_request.collection_name,
            ids=delete_request.ids,
            filter=delete_request.filter,
        )
        return VectorDeleteResponse(
            success=success,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting vectors: {str(e)}",
        )

@router.post("/embedding")
async def get_embedding_endpoint(request: Request, text: str):
    """
    Get embedding for a text
    """
    try:
        embedding = await get_embedding(text)
        return {"embedding": embedding}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting embedding: {str(e)}",
        )
