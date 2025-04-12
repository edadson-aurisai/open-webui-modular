from fastapi import APIRouter, Depends, HTTPException, Request, Response
import httpx
from typing import Any, Dict

from app.core.config import settings
from app.services.proxy import proxy_request

router = APIRouter()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def agent_proxy(request: Request, path: str):
    """
    Proxy requests to the agent service
    """
    # Map the path to the correct endpoint
    if path == "tools":
        path = "api/v1/tools/"
    elif path.startswith("tools/"):
        path = f"api/v1/{path}"
    elif path == "tasks":
        path = "api/v1/tasks/"
    elif path.startswith("tasks/"):
        path = f"api/v1/{path}"
    elif path == "pipelines":
        path = "api/v1/pipelines/"
    elif path.startswith("pipelines/"):
        path = f"api/v1/{path}"
    elif path == "code":
        path = "api/v1/code/"
    elif path.startswith("code/"):
        path = f"api/v1/{path}"

    return await proxy_request(
        request=request,
        service_url=settings.agent_service_url,
        path=path
    )
