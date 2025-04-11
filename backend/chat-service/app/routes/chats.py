from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.chats import (
    ChatCreateRequest,
    ChatCreateResponse,
    ChatUpdateRequest,
    ChatResponse,
    ChatListResponse,
)
from app.services.chats import (
    create_chat,
    update_chat,
    get_chat,
    list_chats,
    delete_chat,
    share_chat,
)
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=ChatCreateResponse)
async def create_chat_endpoint(
    request: Request,
    chat_request: ChatCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Create a new chat
    """
    try:
        chat_id = await create_chat(
            user_id=current_user["sub"],
            title=chat_request.title,
            messages=chat_request.messages,
            models=chat_request.models,
            system=chat_request.system,
            tags=chat_request.tags,
        )
        return ChatCreateResponse(
            id=chat_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating chat: {str(e)}",
        )

@router.get("/", response_model=ChatListResponse)
async def list_chats_endpoint(
    request: Request,
    page: int = 1,
    limit: int = 50,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    List all chats for the current user
    """
    try:
        chats = await list_chats(
            user_id=current_user["sub"],
            page=page,
            limit=limit,
        )
        return ChatListResponse(
            chats=chats,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing chats: {str(e)}",
        )

@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat_endpoint(
    request: Request,
    chat_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Get a chat by ID
    """
    try:
        chat = await get_chat(
            chat_id=chat_id,
            user_id=current_user["sub"],
        )
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )
        return chat
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting chat: {str(e)}",
        )

@router.put("/{chat_id}", response_model=ChatResponse)
async def update_chat_endpoint(
    request: Request,
    chat_id: str,
    chat_request: ChatUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Update a chat
    """
    try:
        chat = await update_chat(
            chat_id=chat_id,
            user_id=current_user["sub"],
            title=chat_request.title,
            messages=chat_request.messages,
            models=chat_request.models,
            system=chat_request.system,
            tags=chat_request.tags,
        )
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )
        return chat
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating chat: {str(e)}",
        )

@router.delete("/{chat_id}", response_model=bool)
async def delete_chat_endpoint(
    request: Request,
    chat_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Delete a chat
    """
    try:
        success = await delete_chat(
            chat_id=chat_id,
            user_id=current_user["sub"],
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )
        return success
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting chat: {str(e)}",
        )

@router.post("/{chat_id}/share", response_model=str)
async def share_chat_endpoint(
    request: Request,
    chat_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Share a chat
    """
    if not settings.enable_chat_sharing:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chat sharing is disabled",
        )
    
    try:
        share_id = await share_chat(
            chat_id=chat_id,
            user_id=current_user["sub"],
        )
        if not share_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )
        return share_id
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sharing chat: {str(e)}",
        )
