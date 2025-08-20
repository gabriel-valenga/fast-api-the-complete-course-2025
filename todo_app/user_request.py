from pydantic import BaseModel, Field

class UserChangePasswordRequest(BaseModel):
    password: str = Field(min_length=4, max_length=128)

    class Config:
        schema_extra = {
            "example": {
                "password": "newsecurepassword"
            }
        }


class UserChangePhoneNumberRequest(BaseModel):
    phone_number: str = Field(min_length=8, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "phone_number": "1234567890"
            }
        }

    
