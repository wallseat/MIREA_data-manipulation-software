from typing import List, Optional
from uuid import UUID

from app.models import Contract, ContractType
from app.schemas.contract import (
    ContractCreate,
    ContractTypeCreate,
    ContractTypeUpdate,
    ContractUpdate,
)
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDContract:
    async def get(
        self,
        session: AsyncSession,
        *,
        organization_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Contract]:
        sel = select(Contract).offset(skip).limit(limit)
        if organization_id:
            sel = sel.where(Contract.organization_id == organization_id)

        result = await session.execute(sel)

        return result.scalars().all()

    async def get_by_id(
        self, session: AsyncSession, *, contract_id: UUID
    ) -> Optional[Contract]:
        result = await session.execute(
            select(Contract).where(Contract.id == contract_id)
        )

        return result.scalars().first()

    async def create(
        self,
        session: AsyncSession,
        *,
        contract_in: ContractCreate,
        organization_id: int,
        type_id: UUID,
    ) -> Contract:
        contract = Contract(
            **contract_in.dict(exclude=["organization_name", "type"]),
            organization_id=organization_id,
            type_id=type_id,
        )

        session.add(contract)
        await session.commit()
        await session.refresh(contract)

        return contract

    async def update(
        self, session: AsyncSession, *, contract: Contract, contract_in: ContractUpdate
    ) -> Contract:
        contract_data = jsonable_encoder(contract)
        update_data = contract_in.dict(skip_defaults=True)

        for field in contract_data:
            if field in update_data:
                setattr(contract, field, update_data[field])

        session.add(contract)
        await session.commit()
        await session.refresh(contract)

        return contract

    async def delete(self, session: AsyncSession, *, contract: Contract) -> None:
        session.delete(contract)
        await session.commit()

    async def get_types(
        self,
        session: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ContractType]:
        result = await session.execute(select(ContractType).offset(skip).limit(limit))

        return result.scalars().all()

    async def get_type(
        self, session: AsyncSession, *, type_: str
    ) -> Optional[ContractType]:
        result = await session.execute(
            select(ContractType).where(ContractType.type == type_)
        )

        return result.scalars().first()

    async def create_type(
        self, session: AsyncSession, *, type_in: ContractTypeCreate
    ) -> ContractType:
        type_ = ContractType(**type_in.dict(by_alias=True))

        session.add(type_)
        await session.commit()
        await session.refresh(type_)

        return type_

    async def update_type(
        self, session: AsyncSession, *, type_: ContractType, type_in: ContractTypeUpdate
    ) -> ContractType:
        type_data = jsonable_encoder(type_)
        update_data = type_in.dict(skip_defaults=True)

        for field in type_data:
            if field in update_data:
                setattr(type_, field, update_data[field])

        session.add(type_)
        await session.commit()
        await session.refresh(type_)

        return type_

    async def delete_type(self, session: AsyncSession, *, type_: ContractType) -> None:
        session.delete(type_)
        await session.commit()


crud_contract = CRUDContract()
