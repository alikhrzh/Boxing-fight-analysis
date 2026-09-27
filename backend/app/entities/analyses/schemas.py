from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.entities.analyses.models import AnalysisStatus
from app.shared.schemas import ApiModel, Pagination


class Point(ApiModel):
    x: float = Field(ge=0)
    y: float = Field(ge=0)


class FighterInitialization(ApiModel):
    frame_index: int = Field(ge=0)
    fighter_a: Point
    fighter_b: Point


class AnalysisConfig(ApiModel):
    ring_polygon: list[Point] | None = Field(default=None, min_length=3)
    fighter_initialization: FighterInitialization | None = None
    pose_model: str = Field(default="yolo11s-pose", max_length=100)


class AnalysisCreate(ApiModel):
    video_id: UUID
    round_number: int = Field(default=1, ge=1, le=99)
    config: AnalysisConfig = Field(default_factory=AnalysisConfig)


class AnalysisRead(ApiModel):
    id: UUID
    video_id: UUID
    round_number: int
    status: AnalysisStatus
    progress: float = Field(ge=0, le=1)
    current_stage: str
    config: dict[str, object]
    result: dict[str, object] | None
    error_code: str | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None
    completed_at: datetime | None


class AnalysisList(ApiModel):
    items: list[AnalysisRead]
    pagination: Pagination
