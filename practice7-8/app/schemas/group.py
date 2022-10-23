from uuid import UUID
from typing import List

from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str


class GroupOut(GroupBase):
    class Config:
        orm_mode = True

    id: UUID


class GroupAddUsers(BaseModel):
    usernames: List[str]


class GroupRemoveUsers(GroupAddUsers):
    pass
