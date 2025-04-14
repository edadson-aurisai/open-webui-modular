from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class CodeExecuteRequest(BaseModel):
    """Code execution request"""
    code: str
    language: str = "python"


class CodeExecuteResponse(BaseModel):
    """Code execution response"""
    result: str


class CodeInterpreterRequest(BaseModel):
    """Code interpreter request"""
    query: str
    context: Optional[str] = None


class CodeInterpreterResponse(BaseModel):
    """Code interpreter response"""
    result: str
