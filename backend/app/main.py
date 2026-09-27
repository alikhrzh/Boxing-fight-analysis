from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.database import Database
from app.core.errors import install_exception_handlers
from app.core.settings import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Application factory used by both Uvicorn and the test suite."""

    app_settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app_settings.ensure_directories()
        database = Database(app_settings.database_url)
        app.state.settings = app_settings
        app.state.database = database
        await database.create_schema()
        try:
            yield
        finally:
            await database.dispose()

    app = FastAPI(
        title=app_settings.app_name,
        version="0.1.0",
        description=(
            "API for uploading boxing footage and managing offline analysis jobs."
        ),
        docs_url="/docs" if app_settings.docs_enabled else None,
        redoc_url="/redoc" if app_settings.docs_enabled else None,
        openapi_url="/openapi.json" if app_settings.docs_enabled else None,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["Accept", "Authorization", "Content-Type"],
    )
    install_exception_handlers(app)
    app.include_router(api_router, prefix=app_settings.api_prefix)
    return app


app = create_app()
