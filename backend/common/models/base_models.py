from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List


class BaseResponse(BaseModel):
    """Base response model for all API responses"""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None


class ErrorResponse(BaseResponse):
    """Error response model"""
    success: bool = False
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class PaginatedResponse(BaseResponse):
    """Paginated response model"""
    total: int
    page: int
    page_size: int
    items: List[Any]
