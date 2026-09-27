from pathlib import Path

from fastapi.testclient import TestClient


def test_upload_and_list_video(
    client: TestClient, tmp_path: Path, uploaded_video: dict[str, object]
) -> None:
    response = client.get("/api/v1/videos")

    assert response.status_code == 200
    payload = response.json()
    assert payload["pagination"]["total"] == 1
    assert payload["items"][0]["id"] == uploaded_video["id"]
    assert payload["items"][0]["original_name"] == "round-one.mp4"
    assert len(list((tmp_path / "uploads").iterdir())) == 1


def test_rejects_unsupported_upload(client: TestClient) -> None:
    response = client.post(
        "/api/v1/videos",
        files={"file": ("notes.txt", b"not-a-video", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "unsupported_video_extension"


def test_delete_video_removes_metadata_and_file(
    client: TestClient, tmp_path: Path, uploaded_video: dict[str, object]
) -> None:
    response = client.delete(f"/api/v1/videos/{uploaded_video['id']}")

    assert response.status_code == 204
    assert client.get(f"/api/v1/videos/{uploaded_video['id']}").status_code == 404
    assert list((tmp_path / "uploads").iterdir()) == []
