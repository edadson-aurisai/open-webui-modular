from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ToolSpec(BaseModel):
    """Tool specification"""
    name: str
    description: str
    parameters: Dict[str, Any]
    returns: Dict[str, Any]


class Tool(BaseModel):
    """Tool"""
    name: str
    description: str
    spec: ToolSpec
    server: Optional[Dict[str, Any]] = None


class ToolListResponse(BaseModel):
    """Tool list response"""
    tools: List[Tool]


class ToolExecuteRequest(BaseModel):
    """Tool execution request"""
    tool_name: str
    params: Dict[str, Any]


class ToolExecuteResponse(BaseModel):
    """Tool execution response"""
    result: Any
