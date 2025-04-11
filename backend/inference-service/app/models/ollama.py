from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class OllamaGenerateRequest(BaseModel):
    model: str
    prompt: str
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[List[int]] = None
    stream: bool = True
    raw: bool = False
    format: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    url_idx: Optional[int] = None


class OllamaChatRequest(BaseModel):
    model: str
    messages: List[Dict[str, Any]]
    stream: bool = True
    format: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    url_idx: Optional[int] = None


class OllamaCompletionRequest(BaseModel):
    model: str
    prompt: str
    stream: bool = True
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    url_idx: Optional[int] = None


class OllamaChatCompletionRequest(BaseModel):
    model: str
    messages: List[Dict[str, Any]]
    stream: bool = True
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    url_idx: Optional[int] = None
