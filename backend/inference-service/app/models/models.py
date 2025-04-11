from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ModelParams(BaseModel):
    """Model parameters"""
    context_length: Optional[int] = None
    embedding_size: Optional[int] = None
    quantization_level: Optional[str] = None
    model_format: Optional[str] = None
    model_family: Optional[str] = None
    model_families: Optional[List[str]] = None
    parameter_size: Optional[str] = None


class ModelMeta(BaseModel):
    """Model metadata"""
    description: Optional[str] = None
    license: Optional[str] = None
    tags: Optional[List[str]] = None
    access_control: Optional[Dict[str, Any]] = None


class ModelResponse(BaseModel):
    """Model response"""
    id: str
    name: str
    owned_by: str
    base_model_id: Optional[str] = None
    params: Optional[ModelParams] = None
    meta: Optional[ModelMeta] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None


class ModelForm(BaseModel):
    """Model creation form"""
    id: str
    name: str
    base_model_id: Optional[str] = None
    params: Optional[ModelParams] = None
    meta: Optional[ModelMeta] = None
