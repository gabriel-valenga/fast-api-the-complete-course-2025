from pydantic import BaseModel, Field
import models


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)
    completed: bool
