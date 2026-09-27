from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.analyses.models import Analysis, AnalysisStatus


class AnalysisRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, analysis: Analysis) -> Analysis:
        self._session.add(analysis)
        await self._session.flush()
        return analysis

    async def get(self, analysis_id: str) -> Analysis | None:
        return await self._session.get(Analysis, analysis_id)

    async def list(
        self,
        *,
        limit: int,
        offset: int,
        status: AnalysisStatus | None = None,
        video_id: str | None = None,
    ) -> tuple[list[Analysis], int]:
        filters = []
        if status is not None:
            filters.append(Analysis.status == status)
        if video_id is not None:
            filters.append(Analysis.video_id == video_id)

        query = (
            select(Analysis)
            .where(*filters)
            .order_by(Analysis.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        count_query = select(func.count()).select_from(Analysis).where(*filters)
        items = list((await self._session.scalars(query)).all())
        total = int(await self._session.scalar(count_query) or 0)
        return items, total
