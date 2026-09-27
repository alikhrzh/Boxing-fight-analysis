from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.entities.analyses.repository import AnalysisRepository
from app.entities.analyses.service import AnalysisService
from app.entities.videos.repository import VideoRepository

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_analysis_service(session: SessionDep) -> AnalysisService:
    return AnalysisService(
        session=session,
        repository=AnalysisRepository(session),
        videos=VideoRepository(session),
    )


AnalysisServiceDep = Annotated[AnalysisService, Depends(get_analysis_service)]
