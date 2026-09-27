from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.entities.health.schemas import HealthRead, ReadinessRead

router = APIRouter(prefix="/health", tags=["health"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/live", response_model=HealthRead)
async def liveness() -> HealthRead:
    return HealthRead(status="ok", service="boxing-analysis-api", version="0.1.0")


@router.get("/ready", response_model=ReadinessRead)
async def readiness(session: SessionDep) -> ReadinessRead:
    await session.execute(text("SELECT 1"))
    return ReadinessRead(
        status="ready",
        database="available",
        analysis_worker="not_configured",
    )
