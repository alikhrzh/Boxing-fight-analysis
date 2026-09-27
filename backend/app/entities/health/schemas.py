from typing import Literal

from app.shared.schemas import ApiModel


class HealthRead(ApiModel):
    status: Literal["ok"]
    service: str
    version: str


class ReadinessRead(ApiModel):
    status: Literal["ready"]
    database: Literal["available"]
    analysis_worker: Literal["not_configured"]
