from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as user_router
from .projects import router as project_router
from .columns import router as column_router
from .boards import router as board_router
from .tasks import router as task_router
from .comments import router as comment_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(task_router)
router.include_router(user_router)
router.include_router(project_router)
router.include_router(column_router)
router.include_router(comment_router)
router.include_router(board_router)


__all__ = [
    'router'
]