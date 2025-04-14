from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class PipelineStep(BaseModel):
    """Pipeline step"""
    id: str
    name: str
    type: str
    config: Dict[str, Any]
    inputs: Dict[str, str]
    outputs: Dict[str, str]


class PipelineBase(BaseModel):
    """Base pipeline model"""
    name: str
    description: Optional[str] = None
    steps: List[PipelineStep]


class PipelineCreateRequest(PipelineBase):
    """Pipeline creation request"""
    pass


class PipelineCreateResponse(BaseModel):
    """Pipeline creation response"""
    id: str


class PipelineUpdateRequest(PipelineBase):
    """Pipeline update request"""
    pass


class PipelineResponse(PipelineBase):
    """Pipeline response"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class PipelineListItem(BaseModel):
    """Pipeline list item"""
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class PipelineListResponse(BaseModel):
    """Pipeline list response"""
    pipelines: List[PipelineListItem]


class PipelineExecuteRequest(BaseModel):
    """Pipeline execution request"""
    pipeline_id: str
    inputs: Dict[str, Any]


class PipelineExecuteResponse(BaseModel):
    """Pipeline execution response"""
    result: Dict[str, Any]
