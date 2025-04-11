from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class TaskType(str, Enum):
    """Task types"""
    CHAT_COMPLETION = "chat_completion"
    FUNCTION_CALLING = "function_calling"
    QUERY_GENERATION = "query_generation"
    TITLE_GENERATION = "title_generation"
    TAG_GENERATION = "tag_generation"
    IMAGE_GENERATION = "image_generation"
    EMOJI_GENERATION = "emoji_generation"
    MOA_COMPLETION = "moa_completion"


class TaskStatus(str, Enum):
    """Task status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskCreateRequest(BaseModel):
    """Task creation request"""
    task_type: TaskType
    params: Dict[str, Any]


class TaskCreateResponse(BaseModel):
    """Task creation response"""
    task_id: str


class TaskStatusResponse(BaseModel):
    """Task status response"""
    task_id: str
    status: TaskStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class TaskListItem(BaseModel):
    """Task list item"""
    task_id: str
    task_type: TaskType
    status: TaskStatus
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    """Task list response"""
    tasks: List[TaskListItem]
