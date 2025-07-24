from pydantic import BaseModel

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    priority: int
    completed: bool

    model_config = {
        "from_attributes": True
    }