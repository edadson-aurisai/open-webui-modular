import logging
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import router as api_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.version,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handling middleware
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception(f"Unhandled exception: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

# Include API routes
app.include_router(api_router, prefix=settings.api_prefix)

# Root endpoint
@app.get("/")
async def root():
    return {
        "service": settings.app_name,
        "version": settings.version,
        "description": "API Gateway for Open WebUI - Entry point for all client requests to microservices",
        "endpoints": {
            "health": "/health - Health check endpoint",
            "api": f"{settings.api_prefix} - API endpoints",
            "docs": "/docs - API documentation",
            "services": {
                "inference": f"{settings.api_prefix}/inference - Inference service endpoints",
                "agent": f"{settings.api_prefix}/agent - Agent service endpoints",
                "retrieval": f"{settings.api_prefix}/retrieval - Retrieval service endpoints",
                "chat": f"{settings.api_prefix}/chat - Chat service endpoints"
            }
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
