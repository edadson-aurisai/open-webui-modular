from fastapi import APIRouter, Depends, HTTPException, Request, Response
from typing import Any, Dict

from app.core.config import settings
from app.services.proxy import proxy_request

router = APIRouter()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def inference_proxy(request: Request, path: str):
    """
    Proxy requests to the inference service
    """
    # Map the path to the correct endpoint
    if path == "models":
        path = "api/v1/models/"
    elif path.startswith("models/"):
        path = f"api/v1/{path}"
    elif path == "ollama":
        path = "api/v1/ollama/"
    elif path.startswith("ollama/"):
        path = f"api/v1/{path}"
    elif path == "openai":
        path = "api/v1/openai/"
    elif path.startswith("openai/"):
        path = f"api/v1/{path}"

    return await proxy_request(
        request=request,
        service_url=settings.inference_service_url,
        path=path
    )
