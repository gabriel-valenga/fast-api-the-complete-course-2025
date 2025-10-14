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
def user_fixture_test():
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


def test_return_user(user_fixture_test):
    response = client.get('/users/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "testuser"
    assert response.json()['email'] == "testuser@test.com"
    assert response.json()['first_name'] == "Test"
    assert response.json()['last_name'] == "User"
    assert response.json()['role'] == "admin"
    assert response.json()['phone_number'] == "1234567890"
    assert response.json()['is_active'] is True


def test_change_password_successful(user_fixture_test):
    response = client.put(
        '/users/change-password',
        json={
            "old_password": "testpassword",
            "new_password": "newtestpassword"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Password updated successfully"}
    db = TestingSessionLocal()
    user = db.query(User).filter(User.username == "testuser").first()
    assert bcrypt_context.verify("newtestpassword", user.hashed_password)
    db.close()


def test_change_password_invalid_old_password(user_fixture_test):
    response = client.put(
        '/users/change-password',
        json={
            "old_password": "wrong_password",
            "new_password": "newtestpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


def test_change_phone_number_successful(user_fixture_test):
    response = client.put(
        '/users/change-phone-number',
        json={
            "new_phone_number": "0987654321"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Phone number updated successfully"}
    db = TestingSessionLocal()
    user = db.query(User).filter(User.username == "testuser").first()
    assert user.phone_number == "0987654321"
    db.close()
    