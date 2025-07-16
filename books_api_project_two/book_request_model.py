from typing import Optional
from pydantic import BaseModel, Field


class BookRequestModelBase(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, description="The title of the book")
    author: Optional[str] = Field(default=None, min_length=1, description="The author of the book")
    description: Optional[str] = Field(default=None, min_length=1, max_length=100, description="A short description of the book")
    rating: Optional[int] = Field(default=None, gt=-1, lt=6, description="Book rating from 0 to 5")
    published_year: Optional[int] = Field(default=None, ge=1450, le=2025, description="Year the book was published")


class CreateBookRequestModel(BookRequestModelBase):
    title: str = Field(min_length=3, description=BookRequestModelBase.model_fields['title'].description)
    author: str = Field(min_length=1, description=BookRequestModelBase.model_fields['author'].description)
    description: str = Field(min_length=1, max_length=100, description=BookRequestModelBase.model_fields['description'].description)
    rating: int = Field(gt=-1, lt=6, description=BookRequestModelBase.model_fields['rating'].description)
    published_year: int = Field(ge=1450, le=2025, description=BookRequestModelBase.model_fields['published_year'].description)


class UpdateBookRequestModel(BookRequestModelBase):
    pass

