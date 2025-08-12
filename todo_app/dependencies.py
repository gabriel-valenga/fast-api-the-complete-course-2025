from typing import Annotated, Tuple
from fastapi import Depends, HTTPException, status
from database import get_db
from sqlalchemy.orm import Session
from routers.auth import get_current_user, get_db_and_current_user


def get_db_and_user(
    db_and_user: Tuple[Session, dict] = Depends(get_db_and_current_user)
) -> Tuple[Session, dict]:
    db, user = db_and_user
    return db, user


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
db_and_user_dependency = Annotated[Tuple[Session, dict], Depends(get_db_and_user)]


def admin_check(user: dict = Depends(get_current_user)):
    if user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource."
        )
    return user


admin_dependency = Annotated[dict, Depends(admin_check)]





