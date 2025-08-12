from fastapi import HTTPException, Path, APIRouter
from sqlalchemy.orm import Session
from user_response import UserResponse
from .auth import hash_password
from dependencies import db_dependency, user_dependency, db_and_user_dependency, admin_dependency
from models import User as UserModel

router = APIRouter()

def return_user_filtering_by_id(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
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
    users = db.query(UserModel).all()
    return {"users": [UserResponse.model_validate(u).model_dump() for u in users]}



@router.put("/user/{user_id}/change_password")
async def change_user_password(
    _: admin_dependency,
    db: db_dependency, 
    user_id: int, 
    new_password: str= Path(min_length=4, max_length=128)
):
    user_data = return_user_filtering_by_id(db, user_id)
    user_data.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user_data)
    return {"message": "Password updated successfully."}


@router.put("/current_user/change_password")
async def change_current_user_password(
    db_and_user:db_and_user_dependency, new_password: str
):
    db, user = db_and_user
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return {"message": "Password updated successfully."}
