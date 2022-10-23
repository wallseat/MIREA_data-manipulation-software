from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi.encoders import jsonable_encoder

from app.models import EquipmentBalance, EquipmentPosition
from app.schemas.equipment import (
    EquipmentCreate,
    EquipmentPositionCreate,
    EquipmentPositionUpdate,
)


class CRUDEquipment:
    async def get_equipment_positions(
        self,
        session: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[EquipmentPosition]:
        result = await session.execute(
            select(EquipmentPosition).limit(limit).offset(skip)
        )

        return result.scalars().all()

    async def get_equipment_position_by_name(
        self,
        session: AsyncSession,
        *,
        name: str,
    ) -> List[EquipmentPosition]:
        result = await session.execute(
            select(EquipmentPosition).where(EquipmentPosition.name == name)
        )

        return result.scalars().first()

    async def create_equipment_position(
        self, session: AsyncSession, *, equipment_position_in: EquipmentPositionCreate
    ) -> EquipmentPosition:

        equipment_position = EquipmentPosition(**equipment_position_in.dict())
        session.add(equipment_position)

        await session.commit()
        await session.refresh(equipment_position)

        return equipment_position

    async def update_equipment_position(
        self,
        session: AsyncSession,
        *,
        equipment_position: EquipmentPosition,
        equipment_position_in: EquipmentPositionUpdate,
    ) -> EquipmentPosition:
        organization_data = jsonable_encoder(equipment_position)
        update_data = equipment_position_in.dict(skip_defaults=True)

        for field in organization_data:
            if field in update_data:
                setattr(equipment_position, field, update_data[field])

        session.add(equipment_position)
        await session.commit()
        await session.refresh(equipment_position)

        return equipment_position

    async def delete_equipment_position(
        self,
        session: AsyncSession,
        *,
        equipment_position: EquipmentPosition,
    ) -> None:
        session.delete(equipment_position)
        await session.commit()

    async def get_equipment_balance_by_position(
        self,
        session: AsyncSession,
        *,
        equipment_position: EquipmentPosition,
        skip: int = 0,
        limit: int = 100,
    ) -> List[EquipmentBalance]:
        result = await session.execute(
            select(EquipmentBalance)
            .where(EquipmentBalance.position_id == equipment_position.id)
            .offset(skip)
            .limit(limit)
        )

        return result.scalars().all()

    async def get_equipment_balance_by_position_serial_number(
        self,
        session: AsyncSession,
        *,
        equipment_position: EquipmentPosition,
        serial_number: str,
    ) -> List[EquipmentBalance]:
        result = await session.execute(
            select(EquipmentBalance).where(
                and_(
                    EquipmentBalance.position_id == equipment_position.id,
                    EquipmentBalance.serial_number == serial_number,
                )
            )
        )

        return result.scalars().first()

    async def create_equipment_balance(
        self,
        session: AsyncSession,
        *,
        equipment_position: EquipmentPosition,
        equipment_balance_in: EquipmentCreate,
    ) -> EquipmentPosition:
        equipment_position = EquipmentBalance(
            **equipment_balance_in.dict(), position_id=equipment_position.ids
        )
        session.add(equipment_position)

        await session.commit()
        await session.refresh(equipment_position)

        return equipment_position

    async def delete_equipment_balance(
        self,
        session: AsyncSession,
        *,
        equipment_balance: EquipmentBalance,
    ) -> List[EquipmentBalance]:
        session.delete(equipment_balance)
        await session.commit()


crud_equipment = CRUDEquipment()
