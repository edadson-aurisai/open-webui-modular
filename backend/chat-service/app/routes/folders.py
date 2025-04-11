from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.folders import (
    FolderCreateRequest,
    FolderCreateResponse,
    FolderUpdateRequest,
    FolderResponse,
    FolderListResponse,
)
from app.services.folders import (
    create_folder,
    update_folder,
    get_folder,
    list_folders,
    delete_folder,
)
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=FolderCreateResponse)
async def create_folder_endpoint(
    request: Request,
    folder_request: FolderCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Create a new folder
    """
    try:
        folder_id = await create_folder(
            user_id=current_user["sub"],
            name=folder_request.name,
            description=folder_request.description,
        )
        return FolderCreateResponse(
            id=folder_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating folder: {str(e)}",
        )

@router.get("/", response_model=FolderListResponse)
async def list_folders_endpoint(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    List all folders for the current user
    """
    try:
        folders = await list_folders(
            user_id=current_user["sub"],
        )
        return FolderListResponse(
            folders=folders,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing folders: {str(e)}",
        )

@router.get("/{folder_id}", response_model=FolderResponse)
async def get_folder_endpoint(
    request: Request,
    folder_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Get a folder by ID
    """
    try:
        folder = await get_folder(
            folder_id=folder_id,
            user_id=current_user["sub"],
        )
        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Folder not found",
            )
        return folder
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting folder: {str(e)}",
        )

@router.put("/{folder_id}", response_model=FolderResponse)
async def update_folder_endpoint(
    request: Request,
    folder_id: str,
    folder_request: FolderUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Update a folder
    """
    try:
        folder = await update_folder(
            folder_id=folder_id,
            user_id=current_user["sub"],
            name=folder_request.name,
            description=folder_request.description,
        )
        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Folder not found",
            )
        return folder
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating folder: {str(e)}",
        )

@router.delete("/{folder_id}", response_model=bool)
async def delete_folder_endpoint(
    request: Request,
    folder_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Delete a folder
    """
    try:
        success = await delete_folder(
            folder_id=folder_id,
            user_id=current_user["sub"],
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Folder not found",
            )
        return success
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting folder: {str(e)}",
        )
