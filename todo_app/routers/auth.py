from datetime import timedelta, datetime, timezone  # Import datetime for token expiration
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from database import session_local
from sqlalchemy.orm import Session
from models import User
from passlib.context import CryptContext
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError  # For JWT token creation and validation


SECRET_KEY = '252dee40692e493794a122057e2c91f11ae047b55c2445728e5533b9aae93eb0'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 20  # Token validity duration in minutes

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme setup, points to the token URL for Swagger UI "Authorize" button
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


# Dependency to get DB session, ensures session is closed after request
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
    last_name: str | None = None
    password: str
    roles: str = "user"  # Default user role


# Extracts and validates current user from JWT token
def get_current_user(db: db_dependency, token: str = Depends(oauth2_bearer)):
    try:
        # Decode JWT token using secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")  # User ID stored in token payload
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except JWTError:
        # JWT token is invalid or expired
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    

@router.get("/auth/get_user/")
async def get_user(current_user: Annotated[User, Depends(get_current_user)]):
    # Returns current authenticated user's username
    return {"message": "User authenticated successfully", "user": current_user.username}


# Creates a JWT token for a given user with expiration
def create_access_token(username: str, user_id: int, expires_delta: timedelta = None):
    to_encode = {"sub": username, "id": user_id}
    # Set token expiration time (current UTC time + expires_delta)
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(seconds=3600))
    to_encode.update({"exp": expire})

    # Encode JWT token using SECRET_KEY and ALGORITHM
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/auth/create_user/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user: CreateUserRequest):
    create_user_model = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=bcrypt_context.hash(user.password),
        roles=user.roles,
        is_active=True
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)  # Refresh instance to get updated fields (e.g., id)
    return create_user_model


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None  # User not found
    if not bcrypt_context.verify(password, user.hashed_password):
        return None  # Password does not match
    return user  # Authentication successful


# Endpoint to login and receive JWT access token
@router.post("/auth/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    # Authenticate user with username and password from form data
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        # Raise 401 Unauthorized if authentication fails
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token with expiration time
    token = create_access_token(
        username=user.username,
        user_id=user.id,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Return the token and token type as per OAuth2 spec
    return {
        "access_token": token,
        "token_type": "bearer"
    }
