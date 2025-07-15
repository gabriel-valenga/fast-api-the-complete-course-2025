from typing import Optional
from pydantic import BaseModel, Field

class CreateBookRequestModel(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)


class UpdateBookRequestModel(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3)
    author: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1, max_length=100)
    rating: Optional[int] = Field(default=None, gt=-1, lt=6)

