from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.settings import Settings
from app.core.storage import LocalVideoStorage
from app.entities.videos.repository import VideoRepository
from app.entities.videos.service import VideoService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_video_service(session: SessionDep, request: Request) -> VideoService:
    settings: Settings = request.app.state.settings
    return VideoService(
        session=session,
        repository=VideoRepository(session),
        storage=LocalVideoStorage(settings),
    )


VideoServiceDep = Annotated[VideoService, Depends(get_video_service)]
