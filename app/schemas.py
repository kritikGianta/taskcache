from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    priority: str = "medium"

class TaskResponse(BaseModel):
    id: int
    title: str
    priority: str
    status: str