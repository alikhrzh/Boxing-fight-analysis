from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.core.storage import LocalVideoStorage
from app.entities.videos.models import Video
from app.entities.videos.repository import VideoRepository


class VideoService:
    def __init__(
        self,
        session: AsyncSession,
        repository: VideoRepository,
        storage: LocalVideoStorage,
    ) -> None:
        self._session = session
        self._repository = repository
        self._storage = storage

    async def upload(self, upload: UploadFile) -> Video:
        stored = await self._storage.save(upload)
        video = Video(
            id=str(uuid4()),
            original_name=stored.original_name,
            stored_name=stored.stored_name,
            content_type=stored.content_type,
            size_bytes=stored.size_bytes,
            sha256=stored.sha256,
        )
        try:
            await self._repository.add(video)
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            self._storage.delete(stored.stored_name)
            raise
        return video

    async def get(self, video_id: str) -> Video:
        video = await self._repository.get(video_id)
        if video is None:
            raise NotFoundError("video", video_id)
        return video

    async def list(self, *, limit: int, offset: int) -> tuple[list[Video], int]:
        return await self._repository.list(limit=limit, offset=offset)

    async def content(self, video_id: str) -> tuple[Video, Path]:
        video = await self.get(video_id)
        return video, self._storage.resolve(video.stored_name)

    async def delete(self, video_id: str) -> None:
        video = await self.get(video_id)
        stored_name = video.stored_name
        await self._repository.delete(video)
        await self._session.commit()
        self._storage.delete(stored_name)
