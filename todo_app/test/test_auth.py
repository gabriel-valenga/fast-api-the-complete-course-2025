import pytest
from sqlalchemy import text
from fastapi.testclient import TestClient
from fastapi import HTTPException
from ..database import get_db
from ..main import app
from ..routers.auth import (
    get_current_user, 
    authenticate_user, 
    create_access_token, 
    SECRET_KEY, 
    ALGORITHM
)
from ..routers.todos import get_db_and_user
from ..models import Todos
from .utils import (
    TestingSessionLocal, 
    engine, 
    override_get_db, 
    override_get_current_user, 
    override_get_db_and_user
)
from jose import jwt
from datetime import timedelta

app.dependency_overrides[get_db] = override_get_db 
app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db_and_user] = override_get_db_and_user 

client = TestClient(app)


def test_authenticate_user(user_fixture_test):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(db, "testuser", "testpassword")
    assert authenticated_user is not None
    assert authenticated_user.username == user_fixture_test.username

    non_existent_user = authenticate_user(db, "wronguser", "testpassword")
    assert non_existent_user is False

    wrong_password_user = authenticate_user(db, "testuser", "wrongpassword")
    assert wrong_password_user is False


def test_create_access_token():
    username = "testuser"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)
    token = create_access_token(
        username=username, 
        user_id=user_id,
        role=role,
        expires_delta=expires_delta
    )
    decoded_token = jwt.decode(
        token, 
        SECRET_KEY, 
        algorithms=[ALGORITHM],
        options={"verify_signature": False}
    )
    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {
        "sub": "testuser",
        "id": 1,
        "role": "user"
    }
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {"username": "testuser", "id": 1, "user_role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {
        "role": "user"
    } 
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=token)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"
    