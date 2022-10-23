from uuid import UUID
from typing import Optional

from pydantic import BaseModel, validator


class ContactPersonBase(BaseModel):
    first_name: str
    second_name: str
    email: str
    tel: Optional[str] = None

    @validator("first_name")
    def first_name_to_lower(cls, v: str) -> str:
        return v.lower()

    @validator("second_name")
    def second_name_to_lower(cls, v: str) -> str:
        return v.lower()


class ContactPersonCreate(ContactPersonBase):
    organization_name: str


class ContactPersonUpdate(ContactPersonBase):
    first_name: Optional[str]
    second_name: Optional[str]
    email: Optional[str]
    organization_name: Optional[str]


class ContactPersonOut(ContactPersonBase):
    class Config:
        orm_mode = True

    id: UUID
    organization_id: UUID
