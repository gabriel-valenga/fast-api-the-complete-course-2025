from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username: str
    email: str  
    role: str
    firstname: str
    lastname: str = ''
    is_active: bool

    model_config = {
        "from_attributes": True
    }