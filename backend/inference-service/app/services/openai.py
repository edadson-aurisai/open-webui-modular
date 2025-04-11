import aiohttp
import json
import logging
from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse, JSONResponse

from app.core.config import settings

logger = logging.getLogger(__name__)

AIOHTTP_CLIENT_TIMEOUT = 600  # 10 minutes


async def cleanup_response(response, session):
    """
    Clean up the response and session
    """
    await response.release()
    await session.close()


def openai_o1_o3_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle special cases for o1/o3 models
    """
    if "max_tokens" in payload:
        payload["max_completion_tokens"] = payload["max_tokens"]
        del payload["max_tokens"]
    return payload


async def send_post_request(
    url: str,
    payload: Any,
    key: str,
    stream: bool = False,
) -> Any:
    """
    Send a POST request to OpenAI
    """
    try:
        session = aiohttp.ClientSession(
            trust_env=True, 
            timeout=aiohttp.ClientTimeout(total=AIOHTTP_CLIENT_TIMEOUT)
        )
        
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }
        
        # Add special headers for OpenRouter
        if "openrouter.ai" in url:
            headers.update({
                "HTTP-Referer": "https://openwebui.com/",
                "X-Title": "Open WebUI",
            })
        
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
        logger.error(f"Error connecting to OpenAI: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error connecting to OpenAI: {str(e)}",
        )
