from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, File, Query, Response, UploadFile, status
from fastapi.responses import FileResponse

from app.entities.videos.dependencies import VideoServiceDep
from app.entities.videos.schemas import VideoList, VideoRead
from app.shared.schemas import Pagination

router = APIRouter(prefix="/videos", tags=["videos"])


@router.post("", response_model=VideoRead, status_code=status.HTTP_201_CREATED)
async def upload_video(
    service: VideoServiceDep,
    file: Annotated[UploadFile, File(description="Boxing round video")],
) -> VideoRead:
    return VideoRead.model_validate(await service.upload(file))


@router.get("", response_model=VideoList)
async def list_videos(
    service: VideoServiceDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 25,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> VideoList:
    items, total = await service.list(limit=limit, offset=offset)
    return VideoList(
        items=[VideoRead.model_validate(item) for item in items],
        pagination=Pagination(limit=limit, offset=offset, total=total),
    )


@router.get("/{video_id}", response_model=VideoRead)
async def get_video(video_id: UUID, service: VideoServiceDep) -> VideoRead:
    return VideoRead.model_validate(await service.get(str(video_id)))


@router.get("/{video_id}/content", response_class=FileResponse)
async def get_video_content(video_id: UUID, service: VideoServiceDep) -> FileResponse:
    video, path = await service.content(str(video_id))
    return FileResponse(
        path,
        media_type=video.content_type or "application/octet-stream",
        filename=video.original_name,
        content_disposition_type="inline",
    )


@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(video_id: UUID, service: VideoServiceDep) -> Response:
    await service.delete(str(video_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
