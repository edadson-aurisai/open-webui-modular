from fastapi import APIRouter
from app.routes import ollama, openai, models

router = APIRouter()

router.include_router(ollama.router, prefix="/ollama", tags=["ollama"])
router.include_router(openai.router, prefix="/openai", tags=["openai"])
router.include_router(models.router, prefix="/models", tags=["models"])
