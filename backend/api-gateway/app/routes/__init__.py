from fastapi import APIRouter
from app.routes import inference, agent, retrieval, chat

router = APIRouter()

router.include_router(inference.router, prefix="/inference", tags=["inference"])
router.include_router(agent.router, prefix="/agent", tags=["agent"])
router.include_router(retrieval.router, prefix="/retrieval", tags=["retrieval"])
router.include_router(chat.router, prefix="/chat", tags=["chat"])
