from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.pipelines import (
    PipelineCreateRequest,
    PipelineCreateResponse,
    PipelineUpdateRequest,
    PipelineResponse,
    PipelineListResponse,
    PipelineExecuteRequest,
    PipelineExecuteResponse,
)
from app.services.pipelines import (
    create_pipeline,
    update_pipeline,
    get_pipeline,
    list_pipelines,
    delete_pipeline,
    execute_pipeline,
)
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=PipelineCreateResponse)
async def create_pipeline_endpoint(
    request: Request,
    pipeline_request: PipelineCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Create a new pipeline
    """
    try:
        pipeline_id = await create_pipeline(
            user_id=current_user["sub"],
            name=pipeline_request.name,
            description=pipeline_request.description,
            steps=pipeline_request.steps,
        )
        return PipelineCreateResponse(
            id=pipeline_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating pipeline: {str(e)}",
        )

@router.get("/", response_model=PipelineListResponse)
async def list_pipelines_endpoint(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    List all pipelines for the current user
    """
    try:
        pipelines = await list_pipelines(
            user_id=current_user["sub"],
        )
        return PipelineListResponse(
            pipelines=pipelines,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing pipelines: {str(e)}",
        )

@router.get("/{pipeline_id}", response_model=PipelineResponse)
async def get_pipeline_endpoint(
    request: Request,
    pipeline_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Get a pipeline by ID
    """
    try:
        pipeline = await get_pipeline(
            pipeline_id=pipeline_id,
            user_id=current_user["sub"],
        )
        if not pipeline:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pipeline not found",
            )
        return pipeline
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting pipeline: {str(e)}",
        )

@router.put("/{pipeline_id}", response_model=PipelineResponse)
async def update_pipeline_endpoint(
    request: Request,
    pipeline_id: str,
    pipeline_request: PipelineUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Update a pipeline
    """
    try:
        pipeline = await update_pipeline(
            pipeline_id=pipeline_id,
            user_id=current_user["sub"],
            name=pipeline_request.name,
            description=pipeline_request.description,
            steps=pipeline_request.steps,
        )
        if not pipeline:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pipeline not found",
            )
        return pipeline
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating pipeline: {str(e)}",
        )

@router.delete("/{pipeline_id}", response_model=bool)
async def delete_pipeline_endpoint(
    request: Request,
    pipeline_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Delete a pipeline
    """
    try:
        success = await delete_pipeline(
            pipeline_id=pipeline_id,
            user_id=current_user["sub"],
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pipeline not found",
            )
        return success
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting pipeline: {str(e)}",
        )

@router.post("/execute", response_model=PipelineExecuteResponse)
async def execute_pipeline_endpoint(
    request: Request,
    execute_request: PipelineExecuteRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Execute a pipeline
    """
    try:
        result = await execute_pipeline(
            pipeline_id=execute_request.pipeline_id,
            user_id=current_user["sub"],
            inputs=execute_request.inputs,
        )
        return PipelineExecuteResponse(
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
            detail=f"Error executing pipeline: {str(e)}",
        )
