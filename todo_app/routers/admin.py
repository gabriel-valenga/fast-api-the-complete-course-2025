from typing import Annotated
from fastapi import Depends, HTTPException, Path, status, APIRouter
from database import session_local
from sqlalchemy.orm import Session
from todo_response import TodoResponse
from todo_request import TodoRequest
from .auth import get_current_user
import models

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


async def admin_dependency(user: user_dependency) -> dict:
    if user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource."
        )
    return user
