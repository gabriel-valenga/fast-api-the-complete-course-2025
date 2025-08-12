from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username: str
    email: str  
    role: str
    first_name: str
    lastname: str = ''
    is_active: bool

    model_config = {
        "from_attributes": True
    }