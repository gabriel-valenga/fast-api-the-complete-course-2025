import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from ..models import User
from ..main import app
from ..database import get_db
from ..routers.auth import get_current_user
from ..routers.todos import get_db_and_user
from .utils import (
    TestingSessionLocal, 
    override_get_db, 
    override_get_current_user, 
    override_get_db_and_user,
    engine
)
from ..routers.auth import bcrypt_context
from fastapi import status 


client = TestClient(app)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db_and_user] = override_get_db_and_user


@pytest.fixture
def test_user():
    print("Setting up test user")
    user = User(
        username="testuser", 
        email="testuser@test.com",
        first_name="Test",
        last_name="User",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="1234567890",
        is_active=True
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


def test_return_user(test_user):
    response = client.get('/current_user_information/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "testuser"
