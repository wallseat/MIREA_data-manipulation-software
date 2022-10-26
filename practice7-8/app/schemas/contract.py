from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ContractBase(BaseModel):
    name: str
    description: str
    price: float


class ContractCreate(ContractBase):
    organization_name: str
    type_: str = Field(alias="type")


class ContractUpdate(ContractBase):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]


class ContractOut(ContractBase):
    class Config:
        orm_mode = True

    id: UUID
    organization_id: UUID
    type_id: UUID


class ContractTypeBase(BaseModel):
    type_: str = Field(alias="type")


class ContractTypeCreate(ContractTypeBase):
    pass


class ContractTypeUpdate(ContractTypeBase):
    pass


class ContractTypeOut(ContractTypeBase):
    class Config:
        orm_mode = True

    id: UUID
