from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router

api_router = APIRouter()


@api_router.get("/health")
async def health_check():
    return {"status": "healthy"}


api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
