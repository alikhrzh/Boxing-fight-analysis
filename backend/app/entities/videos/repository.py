from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.videos.models import Video


class VideoRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, video: Video) -> Video:
        self._session.add(video)
        await self._session.flush()
        return video

    async def get(self, video_id: str) -> Video | None:
        return await self._session.get(Video, video_id)

    async def list(self, *, limit: int, offset: int) -> tuple[list[Video], int]:
        query = (
            select(Video).order_by(Video.created_at.desc()).limit(limit).offset(offset)
        )
        count_query = select(func.count()).select_from(Video)
        items = list((await self._session.scalars(query)).all())
        total = int(await self._session.scalar(count_query) or 0)
        return items, total

    async def delete(self, video: Video) -> None:
        await self._session.delete(video)
