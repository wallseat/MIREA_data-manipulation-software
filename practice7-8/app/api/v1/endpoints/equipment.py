from typing import List

from app.api.providers import RoleChecker, get_session
from app.core.http_exceptions import x_already_exists_exception, x_not_found_exception
from app.crud.equipment import crud_equipment
from app.schemas.equipment import (
    EquipmentCreate,
    EquipmentOut,
    EquipmentPositionCreate,
    EquipmentPositionOut,
    EquipmentPositionUpdate,
)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
admin_only = RoleChecker(["admin"])

equipment_position_ae = x_already_exists_exception("Equipment position")
equipment_position_nf = x_not_found_exception("Equipment position")
equipment_balance_nf = x_not_found_exception("Equipment balance")
equipment_balance_ae = x_already_exists_exception("Equipment balance")


@router.get("/", response_model=List[EquipmentPositionOut])
async def get_equipment_positions(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
):
    """
    Get all equipment positions
    """
    equipment_positions = await crud_equipment.get_equipment_positions(
        session, skip=skip, limit=limit
    )
    return equipment_positions


@router.get("/{name}", response_model=EquipmentPositionOut)
async def get_equipment_position(
    name: str,
    session: AsyncSession = Depends(get_session),
):
    """
    Get equipment position by name
    """
    equipment_position = await crud_equipment.get_equipment_position_by_name(
        session, name=name
    )
    if not equipment_position:
        raise equipment_position_nf

    return equipment_position


@router.post("/", response_model=EquipmentPositionOut)
async def create_equipment_position(
    equipment_position_in: EquipmentPositionCreate,
    session: AsyncSession = Depends(get_session),
):
    """
    Create new equipment position
    """
    equipment_position = await crud_equipment.get_equipment_position_by_name(
        session, name=equipment_position_in.name
    )
    if equipment_position:
        raise equipment_position_ae

    equipment_position = await crud_equipment.create_equipment_position(
        session, equipment_position_in=equipment_position_in
    )

    return equipment_position


@router.put("/", response_model=EquipmentPositionOut)
async def update_equipment_position(
    equipment_position_in: EquipmentPositionUpdate,
    session: AsyncSession = Depends(get_session),
):
    """
    Update equipment position
    """
    equipment_position = await crud_equipment.get_equipment_position_by_name(
        session, name=equipment_position_in.name
    )
    if not equipment_position:
        raise equipment_position_nf

    equipment_position = await crud_equipment.update_equipment_position(
        session,
        equipment_position=equipment_position,
        equipment_position_in=equipment_position_in,
    )

    return equipment_position


@router.delete(
    "/{name}",
    status_code=204,
    dependencies=[Depends(admin_only)],
)
async def update_equipment_position(
    name: str,
    session: AsyncSession = Depends(get_session),
):
    """
    Delete equipment position
    """
    equipment_position = await crud_equipment.get_equipment_position_by_name(
        session, name=name
    )
    if not equipment_position:
        raise equipment_position_nf

    equipment_position = await crud_equipment.delete_equipment_position(
        session,
        equipment_position=equipment_position,
    )


@router.get(
    "/balance/{name}",
    response_model=List[EquipmentOut],
)
async def get_balance_by_equipment_name(
    name: str,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
):
    """
    Get equipment balance by equipment position name
    """
    equipment_position = await crud_equipment.get_equipment_position_by_name(
        session, name=name
    )
    if not equipment_position:
        raise equipment_position_nf

    equipment = await crud_equipment.get_equipment_balance_by_position(
        session, skip=skip, limit=limit, equipment_position=equipment_position
    )

    return equipment


@router.post(
    "/balance/{name}",
    response_model=EquipmentOut,
)
async def create_balance_by_equipment_name(
    name: str,
    equipment_balance_in: EquipmentCreate,
    session: AsyncSession = Depends(get_session),
):
    """
    Create new equipment balance by equipment position name
    """
    equipment_position = await crud_equipment.get_equipment_position_by_name(
        session, name=name
    )
    if not equipment_position:
        raise equipment_position_nf

    equipment_balance = (
        await crud_equipment.get_equipment_balance_by_position_serial_number(
            session,
            equipment_position=equipment_position,
            serial_number=equipment_balance_in.serial_number,
        )
    )
    if equipment_balance:
        raise equipment_balance_ae

    equipment_balance = await crud_equipment.create_equipment_balance(
        session,
        equipment_position=equipment_position,
        equipment_balance_in=equipment_balance_in,
    )

    return equipment_balance


@router.delete(
    "/balance/{name}",
    status_code=204,
    dependencies=[Depends(admin_only)],
)
async def delete_balance_by_equipment_name(
    name: str,
    serial_number: str,
    session: AsyncSession = Depends(get_session),
):
    """
    Delete equipment balance by equipment position name and serial number
    """
    equipment_position = await crud_equipment.get_equipment_position_by_name(
        session, name=name
    )
    if not equipment_position:
        raise equipment_position_nf

    equipment_balance = (
        await crud_equipment.get_equipment_balance_by_position_serial_number(
            session,
            equipment_position=equipment_position,
            serial_number=serial_number,
        )
    )
    if not equipment_balance:
        raise equipment_balance_nf

    await crud_equipment.delete_equipment_balance(
        session, equipment_balance=equipment_balance
    )
