from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List, Optional

from app.services.models import get_all_models, get_all_base_models
from app.models.models import ModelResponse

router = APIRouter()

@router.get("/", response_model=List[ModelResponse])
async def list_models(request: Request):
    """
    List all available models
    """
    return await get_all_models()

@router.get("/base", response_model=List[ModelResponse])
async def list_base_models(request: Request):
    """
    List all available base models
    """
    return await get_all_base_models()
