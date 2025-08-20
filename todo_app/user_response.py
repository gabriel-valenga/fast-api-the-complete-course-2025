from typing import Optional
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username: str
    email: str  
    role: str
    first_name: str
    last_name: str = ''
    phone_number: Optional[str] = None
    is_active: bool

    model_config = {
        "from_attributes": True
    }
