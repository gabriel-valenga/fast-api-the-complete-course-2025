import pytest
from sqlalchemy import text
from fastapi.testclient import TestClient
from fastapi import status
from ..database import get_db
from ..main import app
from ..routers.auth import get_current_user
from ..routers.todos import get_db_and_user
from ..models import Todos
from .utils import (
    TestingSessionLocal, 
    engine, 
    override_get_db, 
    override_get_current_user, 
    override_get_db_and_user
)
app.dependency_overrides[get_db] = override_get_db 
app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db_and_user] = override_get_db_and_user 

client = TestClient(app)

@pytest.fixture
def test_todo():
    db = TestingSessionLocal()
    new_todo = Todos(
        title="Test Todo",
        description="This is a test todo", 
        owner_id=1, 
        priority=5,
        completed=False
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    db.close()
    yield new_todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()


def test_read_all_todos_authenticated(test_todo):
    response = client.get('/todos/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "todos": [
            {
                "title": "Test Todo",
                "description": "This is a test todo",
                "id": 1,
                "priority": 5,
                "completed": False
            }
        ]
    }


def test_read_one_todo_authenticated(test_todo):
    response = client.get('todos/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1, 
        'title': 'Test Todo', 
        'description': 'This is a test todo', 
        'priority': 5, 
        'completed': False
    }
    

def test_read_one_todo_authenticated_not_found():
    response = client.get('/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not Found"}


def test_create_todo_authenticated(test_todo):
    request_data = {
        "title": "New Todo", 
        "description": "This is a new todo",
        "priority": 3,
        "completed": False
    }    
    response = client.post(
        '/todos/todo/',
        json=request_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.completed == request_data.get('completed')


def test_update_todo_authenticated(test_todo):
    request_data = {
        "title": "Updated Todo", 
        "description": "This is an updated todo",
        "priority": 4,
        "completed": True
    }    
    response = client.put(
        '/todos/todo/1',
        json=request_data
    )
    assert response.status_code == status.HTTP_200_OK
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "Updated Todo"


def test_update_todo_authenticated_not_found():
    request_data = {
        "title": "Updated Todo", 
        "description": "This is an updated todo",
        "priority": 4,
        "completed": True
    }    
    response = client.put(
        '/todos/todo/999',
        json=request_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}    


def test_delete_todo_authenticated(test_todo):
    response = client.delete('/todos/todo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_authenticated_not_found():
    response = client.delete('/todos/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
    