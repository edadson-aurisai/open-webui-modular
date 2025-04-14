from fastapi import APIRouter
from app.routes import tasks, tools, pipelines, code

router = APIRouter()

router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
router.include_router(tools.router, prefix="/tools", tags=["tools"])
router.include_router(pipelines.router, prefix="/pipelines", tags=["pipelines"])
router.include_router(code.router, prefix="/code", tags=["code"])
