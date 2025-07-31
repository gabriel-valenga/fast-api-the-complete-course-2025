from typing import Annotated
from fastapi import Depends, HTTPException, Path, status, APIRouter
from database import session_local
from sqlalchemy.orm import Session
from todo_response import TodoResponse
from todo_request import TodoRequest
from .auth import get_current_user
import models

router = APIRouter()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def return_todo_filtering_by_id(db: Session, todo_id: int):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.get("/")
async def read_all_todos(db: db_dependency):
    todos = db.query(models.Todos).all()
    return {"todos": [TodoResponse.model_validate(t).model_dump() for t in todos]}


@router.get("/todo/{todo_id}")
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo = return_todo_filtering_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse.model_validate(todo)


@router.post("/todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    todo = models.Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return TodoResponse.model_validate(todo)


@router.put("/todo/{todo_id}")
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo = return_todo_filtering_by_id(db, todo_id)
    for key, value in todo_request.model_dump().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return TodoResponse.model_validate(todo)


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo = return_todo_filtering_by_id(db, todo_id)
    db.delete(todo)
    db.commit()
    return {"detail": "Todo deleted successfully"}
