from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ConflictError, NotFoundError
from app.entities.analyses.models import Analysis, AnalysisStatus
from app.entities.analyses.repository import AnalysisRepository
from app.entities.analyses.schemas import AnalysisCreate
from app.entities.videos.repository import VideoRepository


class AnalysisService:
    def __init__(
        self,
        session: AsyncSession,
        repository: AnalysisRepository,
        videos: VideoRepository,
    ) -> None:
        self._session = session
        self._repository = repository
        self._videos = videos

    async def create(self, command: AnalysisCreate) -> Analysis:
        video_id = str(command.video_id)
        if await self._videos.get(video_id) is None:
            raise NotFoundError("video", video_id)

        analysis = Analysis(
            id=str(uuid4()),
            video_id=video_id,
            round_number=command.round_number,
            status=AnalysisStatus.QUEUED,
            progress=0,
            current_stage="Awaiting analysis worker",
            config=command.config.model_dump(mode="json"),
        )
        await self._repository.add(analysis)
        await self._session.commit()
        return analysis

    async def get(self, analysis_id: str) -> Analysis:
        analysis = await self._repository.get(analysis_id)
        if analysis is None:
            raise NotFoundError("analysis", analysis_id)
        return analysis

    async def list(
        self,
        *,
        limit: int,
        offset: int,
        status: AnalysisStatus | None,
        video_id: str | None,
    ) -> tuple[list[Analysis], int]:
        return await self._repository.list(
            limit=limit,
            offset=offset,
            status=status,
            video_id=video_id,
        )

    async def cancel(self, analysis_id: str) -> Analysis:
        analysis = await self.get(analysis_id)
        if analysis.status == AnalysisStatus.CANCELLED:
            return analysis
        if analysis.status not in {AnalysisStatus.QUEUED, AnalysisStatus.RUNNING}:
            raise ConflictError(
                "analysis_not_cancellable",
                f"An analysis with status '{analysis.status}' cannot be cancelled.",
            )

        now = datetime.now(UTC)
        analysis.status = AnalysisStatus.CANCELLED
        analysis.current_stage = "Cancelled"
        analysis.completed_at = now
        analysis.updated_at = now
        await self._session.commit()
        return analysis
