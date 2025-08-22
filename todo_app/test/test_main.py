from fastapi.testclient import TestClient
from fastapi import status
from todo_app.main import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}

