from typing import Annotated, Tuple
from fastapi import Depends, HTTPException, Path, status, APIRouter
from database import get_db
from sqlalchemy.orm import Session, joinedload
from todo_response import TodoResponse
from todo_request import TodoRequest
from .auth import get_current_user
from models import Todos as TodosModel

router = APIRouter()


def get_db_and_user(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
) -> Tuple[Session, dict]:
    return db, user


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
db_and_user_dependency = Annotated[Tuple[Session, dict], Depends(get_db_and_user)]


def return_todo_filtering_by_id(db: Session, todo_id: int):
    todo = (
        db.query(TodosModel)
        .filter(TodosModel.id == todo_id)
        .first()
    )
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


def return_todo_filtering_by_id_and_user_id(db: Session, todo_id: int, user_id: int):
    todo = (
        db.query(TodosModel)
        .filter(TodosModel.id == todo_id)
        .filter(TodosModel.owner_id == user_id)
        .first()
    )
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.get("/")
async def read_all_todos(db_and_user: db_and_user_dependency):
    db, user = db_and_user
    if user.role != 'admin':
        todos = db.query(TodosModel).filter(TodosModel.owner_id == user.id).all()
    else:
        todos = db.query(TodosModel).options(joinedload(TodosModel.owner)).all()

    return {"todos": [TodoResponse.model_validate(t).model_dump() for t in todos]}


@router.get("/todo/{todo_id}")
async def get_todo_by_id(db_and_user: db_and_user_dependency, todo_id: int = Path(gt=0)):
    db, user = db_and_user
    if user.role != 'admin':
        todo = return_todo_filtering_by_id_and_user_id(db, todo_id, user.id)
    else:
        todo = return_todo_filtering_by_id(db, todo_id)
    return TodoResponse.model_validate(todo)


@router.post("/todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(db_and_user: db_and_user_dependency, todo_request: TodoRequest):
    db, user = db_and_user
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    todo = TodosModel(**todo_request.model_dump(), owner_id=user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return TodoResponse.model_validate(todo)


@router.put("/todo/{todo_id}")
async def update_todo(
        db_and_user: db_and_user_dependency,
        todo_request: TodoRequest, 
        todo_id: int = Path(gt=0)
    ):
    db, user = db_and_user
    if user.role != 'admin':
        todo = return_todo_filtering_by_id_and_user_id(db, todo_id, user.id)
    else:  
        todo = return_todo_filtering_by_id(db, todo_id)
    for key, value in todo_request.model_dump().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return TodoResponse.model_validate(todo)


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
        db_and_user: db_and_user_dependency,
        todo_id: int = Path(gt=0)
    ):
    db, user = db_and_user
    if user.role != 'admin':
        todo = return_todo_filtering_by_id_and_user_id(db, todo_id, user.id)
    else:
        todo = return_todo_filtering_by_id(db, todo_id)
    db.delete(todo)
    db.commit()
    return {"detail": "Todo deleted successfully"}
