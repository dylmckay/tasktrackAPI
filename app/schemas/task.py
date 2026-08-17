from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    description: str


class Task(BaseModel):
    id: int = Field(gt=0)
    description: str
    done: bool


class TaskUpdate(BaseModel):
    description: str | None = None
    done: bool | None = None
