from datetime import datetime
from uuid import UUID

from app.shared.schemas import ApiModel, Pagination


class VideoRead(ApiModel):
    id: UUID
    original_name: str
    content_type: str | None
    size_bytes: int
    sha256: str
    created_at: datetime


class VideoList(ApiModel):
    items: list[VideoRead]
    pagination: Pagination
