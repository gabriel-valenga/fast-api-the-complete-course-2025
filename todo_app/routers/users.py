from typing import Annotated
from fastapi import Depends, HTTPException, Path, APIRouter
from database import session_local
from sqlalchemy.orm import Session
from routers.admin import admin_dependency
from user_response import UserResponse
from .auth import get_current_user, hash_password
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

def return_user_filtering_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/current_user_information/")
async def get_current_user_information(user: user_dependency):
    return {"user": UserResponse.model_validate(user).model_dump()}


@router.get("/user/{user_id}")
async def get_user_by_id(_: admin_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    user_data = return_user_filtering_by_id(db, user_id)
    return {"user": UserResponse.model_validate(user_data).model_dump()}


@router.get("/")
async def read_all_users(_: admin_dependency, db: db_dependency):
    users = db.query(models.User).all()
    return {"users": [UserResponse.model_validate(u).model_dump() for u in users]}



@router.put("/user/{user_id}/change_password")
async def change_user_password(
    _: admin_dependency, db: db_dependency, user_id: int, new_password: str
):
    user_data = return_user_filtering_by_id(db, user_id)
    user_data.hashed_password = hash_password(new_password)
    db.add(user_data)
    db.commit()
    return {"message": "Password updated successfully."}


@router.put("/current_user/change_password")
async def change_current_user_password(
    user: user_dependency, db: db_dependency, new_password: str
):
    user.hashed_password = hash_password(new_password)
    db.add(user)
    db.commit()
    return {"message": "Password updated successfully."}
