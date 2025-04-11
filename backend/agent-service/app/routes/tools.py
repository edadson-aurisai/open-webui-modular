from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.tools import (
    ToolListResponse,
    ToolExecuteRequest,
    ToolExecuteResponse,
)
from app.services.tools import (
    list_tools,
    execute_tool,
)
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=ToolListResponse)
async def list_tools_endpoint(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    List all available tools
    """
    if not settings.enable_tools:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tools are disabled",
        )
    
    try:
        tools = await list_tools()
        return ToolListResponse(
            tools=tools,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing tools: {str(e)}",
        )

@router.post("/execute", response_model=ToolExecuteResponse)
async def execute_tool_endpoint(
    request: Request,
    tool_request: ToolExecuteRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Execute a tool
    """
    if not settings.enable_tools:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tools are disabled",
        )
    
    try:
        result = await execute_tool(
            tool_name=tool_request.tool_name,
            params=tool_request.params,
            user_id=current_user["sub"],
        )
        return ToolExecuteResponse(
            result=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing tool: {str(e)}",
        )
