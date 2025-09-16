from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import base

SQL_ALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "testuser", "id": 1, "user_role": "admin"}


class MockUser:
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role


def override_get_db_and_user():
    db = TestingSessionLocal()
    user = MockUser(id=1, username="testuser", role="user")
    return db, user
