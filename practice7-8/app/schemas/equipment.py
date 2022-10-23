from typing import Optional

from uuid import UUID
from pydantic import BaseModel


class EquipmentPositionBase(BaseModel):
    name: str
    description: Optional[str]
    price: float


class EquipmentPositionCreate(EquipmentPositionBase):
    pass


class EquipmentPositionUpdate(EquipmentPositionBase):
    name: Optional[str]
    price: Optional[float]


class EquipmentPositionOut(EquipmentPositionBase):
    class Config:
        orm_mode = True

    id: UUID


class EquipmentBase(BaseModel):
    serial_number: str


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentOut(EquipmentBase):
    class Config:
        orm_mode = True
    
    id: UUID
    position_id: UUID