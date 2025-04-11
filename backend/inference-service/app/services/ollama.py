import aiohttp
import json
import logging
from typing import Any, Dict, Optional, Tuple
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse, JSONResponse

from app.core.config import settings

logger = logging.getLogger(__name__)

AIOHTTP_CLIENT_TIMEOUT = 600  # 10 minutes


async def get_ollama_url(model: str, url_idx: int = 0) -> Tuple[str, int]:
    """
    Get the Ollama URL for a given model
    """
    if url_idx >= len(settings.ollama_base_urls):
        url_idx = 0
    
    url = settings.ollama_base_urls[url_idx]
    return url, url_idx


async def send_post_request(
    url: str,
    payload: Any,
    key: Optional[str] = None,
    stream: bool = False,
    content_type: str = "application/json",
) -> Any:
    """
    Send a POST request to Ollama
    """
    try:
        session = aiohttp.ClientSession(
            trust_env=True, 
            timeout=aiohttp.ClientTimeout(total=AIOHTTP_CLIENT_TIMEOUT)
        )
        
        headers = {
            "Content-Type": content_type,
        }
        
        if key:
            headers["Authorization"] = f"Bearer {key}"
        
        r = await session.post(
            url=url,
            data=payload,
            headers=headers,
        )
        
        r.raise_for_status()
        
        if stream:
            return StreamingResponse(
                r.content,
                media_type=r.headers.get("Content-Type", "application/json"),
                background=aiohttp.web.BackgroundTask(session.close),
            )
        else:
            response_data = await r.json()
            await session.close()
            return response_data
    
    except aiohttp.ClientError as e:
        logger.error(f"Error connecting to Ollama: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error connecting to Ollama: {str(e)}",
        )
