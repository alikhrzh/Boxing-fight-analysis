from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.entities.analyses.dependencies import AnalysisServiceDep
from app.entities.analyses.models import AnalysisStatus
from app.entities.analyses.schemas import AnalysisCreate, AnalysisList, AnalysisRead
from app.shared.schemas import Pagination

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.post("", response_model=AnalysisRead, status_code=status.HTTP_202_ACCEPTED)
async def create_analysis(
    command: AnalysisCreate, service: AnalysisServiceDep
) -> AnalysisRead:
    return AnalysisRead.model_validate(await service.create(command))


@router.get("", response_model=AnalysisList)
async def list_analyses(
    service: AnalysisServiceDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 25,
    offset: Annotated[int, Query(ge=0)] = 0,
    status_filter: Annotated[AnalysisStatus | None, Query(alias="status")] = None,
    video_id: Annotated[UUID | None, Query()] = None,
) -> AnalysisList:
    items, total = await service.list(
        limit=limit,
        offset=offset,
        status=status_filter,
        video_id=str(video_id) if video_id else None,
    )
    return AnalysisList(
        items=[AnalysisRead.model_validate(item) for item in items],
        pagination=Pagination(limit=limit, offset=offset, total=total),
    )


@router.get("/{analysis_id}", response_model=AnalysisRead)
async def get_analysis(analysis_id: UUID, service: AnalysisServiceDep) -> AnalysisRead:
    return AnalysisRead.model_validate(await service.get(str(analysis_id)))


@router.post("/{analysis_id}/cancel", response_model=AnalysisRead)
async def cancel_analysis(
    analysis_id: UUID, service: AnalysisServiceDep
) -> AnalysisRead:
    return AnalysisRead.model_validate(await service.cancel(str(analysis_id)))
