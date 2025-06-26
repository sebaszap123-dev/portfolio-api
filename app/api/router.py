from fastapi import APIRouter
from app.api.portfolio import router as general_router

router = APIRouter(prefix="/api/v1", tags=["Portfolio"])
router.include_router(general_router)
