from typing import Optional
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: Optional[str] = Field(None, example="本を読む")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    is_done: bool = Field(False, desciption="完了フラグ")


class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True

class TaskUpdateResponse(TaskUpdate):
    id: int

    class Config:
        orm_mode = True

class Task(TaskBase):
    id: int
    is_done: bool = Field(False, description="完了フラグ")

    class Config:
        orm_mode = True
