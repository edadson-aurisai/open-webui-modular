from fastapi import Request, Response
import httpx
import logging
from typing import Any, Dict
from starlette.responses import StreamingResponse

logger = logging.getLogger(__name__)

async def proxy_request(request: Request, service_url: str, path: str) -> Response:
    """
    Proxy a request to a microservice
    """
    # Get request details
    method = request.method
    url = f"{service_url}/{path}"
    headers = dict(request.headers)

    # Remove host header to avoid conflicts
    headers.pop("host", None)

    # Get request body if applicable
    body = await request.body()

    logger.info(f"Proxying {method} request to {url}")

    async with httpx.AsyncClient() as client:
        try:
            # Make the request to the target service
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                content=body,
                timeout=60.0,  # Increased timeout for long-running operations
            )

            # Check if response is streaming
            if "text/event-stream" in response.headers.get("content-type", ""):
                return StreamingResponse(
                    response.aiter_bytes(),
                    status_code=response.status_code,
                    headers=dict(response.headers),
                )

            # Return the response
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
            )
        except httpx.RequestError as e:
            logger.error(f"Error proxying request to {url}: {e}")
            return Response(
                content=f"Error connecting to service: {str(e)}",
                status_code=503,
            )
