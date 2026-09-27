from fastapi import APIRouter

from app.entities.analyses.router import router as analyses_router
from app.entities.health.router import router as health_router
from app.entities.videos.router import router as videos_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(videos_router)
api_router.include_router(analyses_router)
