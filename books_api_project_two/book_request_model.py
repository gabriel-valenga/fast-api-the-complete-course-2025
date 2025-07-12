from pydantic import BaseModel, Field

class BookRequestModel(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)

    