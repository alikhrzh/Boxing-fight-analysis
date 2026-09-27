from fastapi.testclient import TestClient


def test_liveness(client: TestClient) -> None:
    response = client.get("/api/v1/health/live")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "boxing-analysis-api",
        "version": "0.1.0",
    }


def test_readiness_checks_database(client: TestClient) -> None:
    response = client.get("/api/v1/health/ready")

    assert response.status_code == 200
    assert response.json()["database"] == "available"
    assert response.json()["analysis_worker"] == "not_configured"
