from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    description: str = Field(max_length=255)


class Task(BaseModel):
    id: int = Field(gt=0)
    description: str
    done: bool


class TaskUpdate(BaseModel):
    description: str | None = Field(default=None, max_length=255)
    done: bool | None = None
