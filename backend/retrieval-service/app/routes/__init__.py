from fastapi import APIRouter
from app.routes import vector, web, files, knowledge

router = APIRouter()

router.include_router(vector.router, prefix="/vector", tags=["vector"])
router.include_router(web.router, prefix="/web", tags=["web"])
router.include_router(files.router, prefix="/files", tags=["files"])
router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
