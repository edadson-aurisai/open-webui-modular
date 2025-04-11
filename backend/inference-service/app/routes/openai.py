from fastapi import APIRouter, Depends, HTTPException, Request, status, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
import json
import aiohttp
import requests
from typing import Any, Dict, Optional

from app.core.config import settings
from app.services.openai import send_post_request, cleanup_response
from app.models.openai import (
    OpenAIChatCompletionRequest,
    OpenAICompletionRequest,
)

router = APIRouter()

@router.post("/chat/completions")
async def chat_completions(request: Request, form_data: OpenAIChatCompletionRequest):
    """
    Get chat completions from OpenAI
    """
    if not settings.enable_openai_api:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="OpenAI API is disabled",
        )
    
    idx = form_data.idx if form_data.idx is not None else 0
    payload = form_data.model_dump(exclude={"idx"})
    
    url = settings.openai_api_base_urls[idx]
    key = settings.openai_api_keys[idx]
    
    # Handle special cases for different models
    is_o1_o3 = payload["model"].lower().startswith(("o1", "o3-"))
    if is_o1_o3:
        # Special handling for o1/o3 models
        if "max_tokens" in payload:
            payload["max_completion_tokens"] = payload["max_tokens"]
            del payload["max_tokens"]
    elif "api.openai.com" not in url:
        # Remove "max_completion_tokens" for non-OpenAI APIs
        if "max_completion_tokens" in payload:
            payload["max_tokens"] = payload["max_completion_tokens"]
            del payload["max_completion_tokens"]
    
    # Remove redundant fields
    if "max_tokens" in payload and "max_completion_tokens" in payload:
        del payload["max_tokens"]
    
    return await send_post_request(
        url=f"{url}/chat/completions",
        payload=json.dumps(payload),
        key=key,
        stream=payload.get("stream", False),
    )

@router.post("/completions")
async def completions(request: Request, form_data: OpenAICompletionRequest):
    """
    Get completions from OpenAI
    """
    if not settings.enable_openai_api:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="OpenAI API is disabled",
        )
    
    idx = form_data.idx if form_data.idx is not None else 0
    payload = form_data.model_dump(exclude={"idx"})
    
    url = settings.openai_api_base_urls[idx]
    key = settings.openai_api_keys[idx]
    
    return await send_post_request(
        url=f"{url}/completions",
        payload=json.dumps(payload),
        key=key,
        stream=payload.get("stream", False),
    )

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def openai_proxy(request: Request, path: str, background_tasks: BackgroundTasks):
    """
    Proxy requests to OpenAI API
    """
    if not settings.enable_openai_api:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="OpenAI API is disabled",
        )
    
    # Get the OpenAI API key index from query parameters or default to 0
    idx = request.query_params.get("idx", "0")
    try:
        idx = int(idx)
    except ValueError:
        idx = 0
    
    if idx >= len(settings.openai_api_base_urls) or idx >= len(settings.openai_api_keys):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid API key index",
        )
    
    url = settings.openai_api_base_urls[idx]
    key = settings.openai_api_keys[idx]
    
    # Get request body
    body = await request.body()
    
    try:
        session = aiohttp.ClientSession(trust_env=True)
        r = await session.request(
            method=request.method,
            url=f"{url}/{path}",
            data=body,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        r.raise_for_status()
        
        # Check if response is SSE
        if "text/event-stream" in r.headers.get("Content-Type", ""):
            return StreamingResponse(
                r.content,
                status_code=r.status,
                headers=dict(r.headers),
                background=BackgroundTasks(
                    cleanup_response, response=r, session=session
                ),
            )
        else:
            response_data = await r.json()
            return JSONResponse(content=response_data)
    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error connecting to OpenAI API: {str(e)}",
        )
