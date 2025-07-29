from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from database import session_local
from sqlalchemy.orm import Session
from models import User
from passlib.context import CryptContext
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt


SECRET_KEY = '252dee40692e493794a122057e2c91f11ae047b55c2445728e5533b9aae93eb0'
ALGORITHM = 'HS256'
router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = session_local()
    try:
        yield db
    finally:    
        db.close()   

db_dependency = Annotated[Session, Depends(get_db)]   
    

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str = None
    password: str
    role: str = "user"  # Default role is 'user'


@router.get("/auth/get_user/")
async def get_user():
    return {"message": "User authenticated successfully"}


def get_current_user(token: str = Depends(oauth2_bearer), db: db_dependency = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    

def create_access_token(username:str, user_id:int, expires_delta: int = 3600):
    to_encode = {"sub": username, "id": user_id}
    if expires_delta:
        to_encode.update({"exp": jwt.datetime.utcnow() + jwt.timedelta(seconds=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/auth/create_user/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user: CreateUserRequest):
    create_user_model = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=bcrypt_context.hash(user.password),  # In a real application, hash the password
        role=user.role,
        is_active=True  # Default to active
    )
    db.add(create_user_model)
    db.commit()
    return create_user_model


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: db_dependency    
    ):
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            return {"error": "Invalid username or password"}, status.HTTP_401_UNAUTHORIZED
        token = create_access_token(
            username=user.username, 
            user_id=user.id,
            expires_delta=timedelta(minutes=20)
        )
        return {
            "message": "Login successful", 
            "access_token": token, 
            "token_type": "bearer"
        }, status.HTTP_200_OK
