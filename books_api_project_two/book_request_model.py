from pydantic import BaseModel

class BookRequestModel(BaseModel):
    id: int 
    title: str 
    author: str 
    description: str 
    rating: int 

    