from fastapi.testclient import TestClient
from ..main import app
from ..routers import get_db, get_current_user, get_db_and_user
from .utils import override_get_db, override_get_current_user, override_get_db_and_user
from fastapi import status 


client = TestClient(app)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db_and_user] = override_get_db_and_user


def test_return_user():
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is None
