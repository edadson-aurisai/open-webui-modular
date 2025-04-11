from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.tags import (
    TagCreateRequest,
    TagCreateResponse,
    TagUpdateRequest,
    TagResponse,
    TagListResponse,
)
from app.services.tags import (
    create_tag,
    update_tag,
    get_tag,
    list_tags,
    delete_tag,
)
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TagCreateResponse)
async def create_tag_endpoint(
    request: Request,
    tag_request: TagCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Create a new tag
    """
    try:
        tag_id = await create_tag(
            user_id=current_user["sub"],
            name=tag_request.name,
            color=tag_request.color,
        )
        return TagCreateResponse(
            id=tag_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating tag: {str(e)}",
        )

@router.get("/", response_model=TagListResponse)
async def list_tags_endpoint(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    List all tags for the current user
    """
    try:
        tags = await list_tags(
            user_id=current_user["sub"],
        )
        return TagListResponse(
            tags=tags,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing tags: {str(e)}",
        )

@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag_endpoint(
    request: Request,
    tag_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Get a tag by ID
    """
    try:
        tag = await get_tag(
            tag_id=tag_id,
            user_id=current_user["sub"],
        )
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found",
            )
        return tag
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting tag: {str(e)}",
        )

@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag_endpoint(
    request: Request,
    tag_id: str,
    tag_request: TagUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Update a tag
    """
    try:
        tag = await update_tag(
            tag_id=tag_id,
            user_id=current_user["sub"],
            name=tag_request.name,
            color=tag_request.color,
        )
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found",
            )
        return tag
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating tag: {str(e)}",
        )

@router.delete("/{tag_id}", response_model=bool)
async def delete_tag_endpoint(
    request: Request,
    tag_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Delete a tag
    """
    try:
        success = await delete_tag(
            tag_id=tag_id,
            user_id=current_user["sub"],
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found",
            )
        return success
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting tag: {str(e)}",
        )
