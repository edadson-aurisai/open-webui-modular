from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
import json
import aiohttp
from typing import Any, Dict, Optional

from app.core.config import settings
from app.services.ollama import get_ollama_url, send_post_request
from app.models.ollama import (
    OllamaGenerateRequest,
    OllamaChatRequest,
    OllamaCompletionRequest,
    OllamaChatCompletionRequest,
)

router = APIRouter()

@router.post("/generate")
async def generate(request: Request, form_data: OllamaGenerateRequest):
    """
    Generate text using Ollama
    """
    if not settings.enable_ollama_api:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ollama API is disabled",
        )
    
    url_idx = form_data.url_idx if form_data.url_idx is not None else 0
    
    url = settings.ollama_base_urls[url_idx]
    api_config = settings.ollama_api_configs.get(
        str(url_idx),
        settings.ollama_api_configs.get(url, {}),  # Legacy support
    )
    
    prefix_id = api_config.get("prefix_id", None)
    if prefix_id:
        form_data.model = form_data.model.replace(f"{prefix_id}.", "")
    
    return await send_post_request(
        url=f"{url}/api/generate",
        payload=form_data.model_dump_json(exclude_none=True).encode(),
        key=None,  # Ollama doesn't use API keys in the same way
    )

@router.post("/chat")
async def chat(request: Request, form_data: OllamaChatRequest):
    """
    Chat with Ollama
    """
    if not settings.enable_ollama_api:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ollama API is disabled",
        )
    
    url_idx = form_data.url_idx if form_data.url_idx is not None else 0
    payload = form_data.model_dump(exclude={"url_idx"})
    
    if ":" not in payload["model"]:
        payload["model"] = f"{payload['model']}:latest"
    
    url = settings.ollama_base_urls[url_idx]
    api_config = settings.ollama_api_configs.get(
        str(url_idx),
        settings.ollama_api_configs.get(url, {}),  # Legacy support
    )
    
    prefix_id = api_config.get("prefix_id", None)
    if prefix_id:
        payload["model"] = payload["model"].replace(f"{prefix_id}.", "")
    
    return await send_post_request(
        url=f"{url}/api/chat",
        payload=json.dumps(payload),
        stream=form_data.stream,
        content_type="application/x-ndjson",
    )

@router.post("/completions")
async def completions(request: Request, form_data: OllamaCompletionRequest):
    """
    Get completions from Ollama
    """
    if not settings.enable_ollama_api:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ollama API is disabled",
        )
    
    url_idx = form_data.url_idx if form_data.url_idx is not None else 0
    payload = form_data.model_dump(exclude={"url_idx"})
    
    url = settings.ollama_base_urls[url_idx]
    api_config = settings.ollama_api_configs.get(
        str(url_idx),
        settings.ollama_api_configs.get(url, {}),  # Legacy support
    )
    
    prefix_id = api_config.get("prefix_id", None)
    if prefix_id:
        payload["model"] = payload["model"].replace(f"{prefix_id}.", "")
    
    return await send_post_request(
        url=f"{url}/v1/completions",
        payload=json.dumps(payload),
        stream=payload.get("stream", False),
    )

@router.post("/chat/completions")
async def chat_completions(request: Request, form_data: OllamaChatCompletionRequest):
    """
    Get chat completions from Ollama
    """
    if not settings.enable_ollama_api:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ollama API is disabled",
        )
    
    url_idx = form_data.url_idx if form_data.url_idx is not None else 0
    payload = form_data.model_dump(exclude={"url_idx"})
    
    url = settings.ollama_base_urls[url_idx]
    api_config = settings.ollama_api_configs.get(
        str(url_idx),
        settings.ollama_api_configs.get(url, {}),  # Legacy support
    )
    
    prefix_id = api_config.get("prefix_id", None)
    if prefix_id:
        payload["model"] = payload["model"].replace(f"{prefix_id}.", "")
    
    return await send_post_request(
        url=f"{url}/v1/chat/completions",
        payload=json.dumps(payload),
        stream=payload.get("stream", False),
    )
