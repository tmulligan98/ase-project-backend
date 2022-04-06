from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_entrypoint():
    response = client.get(
        "/",
    )
    response_body = response.json()
    assert response.status_code == 200, response.text
    assert response_body["disasterStatus"] is True


def test_healthcheck():
    response = client.get(
        "/health",
    )
    response_body = response.json()
    assert response.status_code == 200, response.text
    assert response_body["status"] == "UP"


def test_handshake():
    response = client.get(
        "api/1/handshake",
    )
    response_body = response.json()
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response_body["host_name"] == "testclient"
