from fastapi import APIRouter, Depends, HTTPException, Request, Response
import httpx
from typing import Any, Dict

from app.core.config import settings
from app.services.proxy import proxy_request

router = APIRouter()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def retrieval_proxy(request: Request, path: str):
    """
    Proxy requests to the retrieval service
    """
    return await proxy_request(
        request=request,
        service_url=settings.retrieval_service_url,
        path=path
    )
