from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, hospitals, \
    departments, surveys, feedbacks, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(hospitals.router, prefix="/hospitals", tags=["hospitals"])
api_router.include_router(departments.router, prefix="/departments", tags=["departments"])
api_router.include_router(surveys.router, prefix="/surveys", tags=["surveys"])
api_router.include_router(feedbacks.router, prefix="/feedbacks", tags=["feedbacks"])
