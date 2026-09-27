from fastapi.testclient import TestClient


def test_create_and_cancel_analysis(
    client: TestClient, uploaded_video: dict[str, object]
) -> None:
    create_response = client.post(
        "/api/v1/analyses",
        json={"video_id": uploaded_video["id"], "round_number": 1},
    )

    assert create_response.status_code == 202
    analysis = create_response.json()
    assert analysis["status"] == "queued"
    assert analysis["current_stage"] == "Awaiting analysis worker"

    cancel_response = client.post(f"/api/v1/analyses/{analysis['id']}/cancel")
    assert cancel_response.status_code == 200
    assert cancel_response.json()["status"] == "cancelled"


def test_analysis_requires_existing_video(client: TestClient) -> None:
    response = client.post(
        "/api/v1/analyses",
        json={"video_id": "44e36934-2a0f-42de-8abb-47d0e2346e00"},
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "video_not_found"


def test_list_analysis_by_status(
    client: TestClient, uploaded_video: dict[str, object]
) -> None:
    client.post(
        "/api/v1/analyses",
        json={"video_id": uploaded_video["id"], "round_number": 2},
    )

    response = client.get("/api/v1/analyses", params={"status": "queued"})

    assert response.status_code == 200
    assert response.json()["pagination"]["total"] == 1
