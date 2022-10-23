from uuid import UUID
from typing import Optional
from datetime import date

from pydantic import BaseModel


class OrganizationBase(BaseModel):
    name: str
    location: str
    postal_code: Optional[str]


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(OrganizationBase):
    name: Optional[str]
    location: Optional[str]


class OrganizationOut(OrganizationBase):
    class Config:
        orm_mode = True

    id: UUID
    first_contract_date: Optional[date]
