from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.code import (
    CodeExecuteRequest,
    CodeExecuteResponse,
    CodeInterpreterRequest,
    CodeInterpreterResponse,
)
from app.services.code import (
    execute_code,
    run_code_interpreter,
)
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/execute", response_model=CodeExecuteResponse)
async def execute_code_endpoint(
    request: Request,
    code_request: CodeExecuteRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Execute code
    """
    if not settings.enable_code_execution:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Code execution is disabled",
        )
    
    try:
        result = await execute_code(
            code=code_request.code,
            language=code_request.language,
            user_id=current_user["sub"],
        )
        return CodeExecuteResponse(
            result=result,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing code: {str(e)}",
        )

@router.post("/interpreter", response_model=CodeInterpreterResponse)
async def code_interpreter_endpoint(
    request: Request,
    interpreter_request: CodeInterpreterRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Run code interpreter
    """
    if not settings.enable_code_interpreter:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Code interpreter is disabled",
        )
    
    try:
        result = await run_code_interpreter(
            query=interpreter_request.query,
            context=interpreter_request.context,
            user_id=current_user["sub"],
        )
        return CodeInterpreterResponse(
            result=result,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error running code interpreter: {str(e)}",
        )
