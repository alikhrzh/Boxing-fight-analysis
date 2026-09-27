from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.settings import Settings
from app.main import create_app


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    settings = Settings(
        data_dir=tmp_path,
        database_url=f"sqlite+aiosqlite:///{tmp_path / 'test.db'}",
        max_upload_bytes=1024 * 1024,
    )
    with TestClient(create_app(settings)) as test_client:
        yield test_client


@pytest.fixture
def uploaded_video(client: TestClient) -> dict[str, object]:
    response = client.post(
        "/api/v1/videos",
        files={"file": ("round-one.mp4", b"fake-video-content", "video/mp4")},
    )
    assert response.status_code == 201
    return response.json()
