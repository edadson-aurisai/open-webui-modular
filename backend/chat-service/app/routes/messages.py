from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.messages import (
    MessageCreateRequest,
    MessageCreateResponse,
    MessageResponse,
    MessageListResponse,
)
from app.services.messages import (
    create_message,
    get_message,
    list_messages,
    delete_message,
)
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=MessageCreateResponse)
async def create_message_endpoint(
    request: Request,
    message_request: MessageCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Create a new message
    """
    try:
        message_id = await create_message(
            user_id=current_user["sub"],
            chat_id=message_request.chat_id,
            content=message_request.content,
            role=message_request.role,
            parent_id=message_request.parent_id,
            model=message_request.model,
        )
        return MessageCreateResponse(
            id=message_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating message: {str(e)}",
        )

@router.get("/", response_model=MessageListResponse)
async def list_messages_endpoint(
    request: Request,
    chat_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    List all messages for a chat
    """
    try:
        messages = await list_messages(
            chat_id=chat_id,
            user_id=current_user["sub"],
        )
        return MessageListResponse(
            messages=messages,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing messages: {str(e)}",
        )

@router.get("/{message_id}", response_model=MessageResponse)
async def get_message_endpoint(
    request: Request,
    message_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Get a message by ID
    """
    try:
        message = await get_message(
            message_id=message_id,
            user_id=current_user["sub"],
        )
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found",
            )
        return message
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting message: {str(e)}",
        )

@router.delete("/{message_id}", response_model=bool)
async def delete_message_endpoint(
    request: Request,
    message_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Delete a message
    """
    try:
        success = await delete_message(
            message_id=message_id,
            user_id=current_user["sub"],
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found",
            )
        return success
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting message: {str(e)}",
        )
