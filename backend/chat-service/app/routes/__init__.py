from fastapi import APIRouter
from app.routes import chats, messages, folders, tags

router = APIRouter()

router.include_router(chats.router, prefix="/chats", tags=["chats"])
router.include_router(messages.router, prefix="/messages", tags=["messages"])
router.include_router(folders.router, prefix="/folders", tags=["folders"])
router.include_router(tags.router, prefix="/tags", tags=["tags"])
