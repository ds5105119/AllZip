from fastapi import APIRouter

from .open_fiscal.api.endpoint.fiscal import router as fiscal_router
from .open_fiscal.api.endpoint.welfare import router as welfare_router
from .user.api.endpoint.user import router as user_router

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(fiscal_router, prefix="/fiscal", tags=["fiscal"])
router.include_router(welfare_router, prefix="/welfare", tags=["welfare"])
