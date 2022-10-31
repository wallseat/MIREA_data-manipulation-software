from typing import Optional
from uuid import UUID

from datetime import date
from pydantic import BaseModel, Field


class BaseTask(BaseModel):
    title: str
    description: Optional[str]
    due_date: Optional[date]
    contract_id: Optional[UUID]
    contact_person_id: UUID


class TaskCreate(BaseTask):
    type_: str = Field(..., alias="type", exclude=True)
    priority: str = Field(..., exclude=True)
    executor_name: str = Field(..., exclude=True)


class TaskUpdate(BaseTask):
    title: Optional[str]
    description: Optional[str]
    type_: Optional[str] = Field(..., alias="type", exclude=True)
    priority: Optional[str] = Field(..., exclude=True)
    executor_name: Optional[str] = Field(..., exclude=True)
    contact_person_id: Optional[UUID]


class TaskOut(BaseTask):
    class Config:
        orm_mode = True

    id: UUID
    close_date: Optional[date]
    open_date: date
    completed: bool
    type_id: UUID
    priority_id: UUID
    author_id: UUID
    executor_id: UUID


class TaskTypeBase(BaseModel):
    type_: str = Field(..., alias="type")


class TaskTypeCreate(TaskTypeBase):
    pass


class TaskTypeOut(TaskTypeBase):
    class Config:
        orm_mode = True

    id: UUID


class TaskPriorityBase(BaseModel):
    priority: str


class TaskPriorityCreate(TaskPriorityBase):
    pass


class TaskPriorityOut(TaskPriorityBase):
    class Config:
        orm_mode = True

    id: UUID
