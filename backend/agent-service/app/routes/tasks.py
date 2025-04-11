from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.tasks import (
    TaskCreateRequest,
    TaskCreateResponse,
    TaskStatusResponse,
    TaskListResponse,
)
from app.services.tasks import (
    create_task,
    get_task_status,
    list_tasks,
    stop_task,
)
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TaskCreateResponse)
async def create_task_endpoint(
    request: Request,
    task_request: TaskCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Create a new task
    """
    try:
        task_id = await create_task(
            user_id=current_user["sub"],
            task_type=task_request.task_type,
            params=task_request.params,
        )
        return TaskCreateResponse(
            task_id=task_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}",
        )

@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status_endpoint(
    request: Request,
    task_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Get the status of a task
    """
    try:
        task_status = await get_task_status(
            task_id=task_id,
            user_id=current_user["sub"],
        )
        if task_status is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        return task_status
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting task status: {str(e)}",
        )

@router.get("/", response_model=TaskListResponse)
async def list_tasks_endpoint(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    List all tasks for the current user
    """
    try:
        tasks = await list_tasks(
            user_id=current_user["sub"],
        )
        return TaskListResponse(
            tasks=tasks,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing tasks: {str(e)}",
        )

@router.delete("/stop/{task_id}", response_model=bool)
async def stop_task_endpoint(
    request: Request,
    task_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Stop a running task
    """
    try:
        success = await stop_task(
            task_id=task_id,
            user_id=current_user["sub"],
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or already completed",
            )
        return success
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error stopping task: {str(e)}",
        )
