from typing import Optional, List
from datetime import date

from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from fastapi.encoders import jsonable_encoder

from app.models import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


class CRUDOrganization:
    async def get_organizations(
        self,
        session: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Organization]:
        result = await session.execute(select(Organization).offset(skip).limit(limit))

        return result.scalars().all()

    async def get_by_name(
        self,
        session: AsyncSession,
        *,
        name: str,
    ) -> Optional[Organization]:
        result = await session.execute(
            select(Organization).where(Organization.name == name)
        )

        return result.scalars().first()

    async def create(
        self,
        session: AsyncSession,
        *,
        organization_in: OrganizationCreate,
    ) -> Organization:
        organization = Organization(**organization_in.dict())
        session.add(organization)
        await session.commit()
        await session.refresh(organization)

        return organization

    async def update(
        self,
        session: AsyncSession,
        *,
        organization: Organization,
        organization_in: OrganizationUpdate,
    ) -> Organization:
        organization_data = jsonable_encoder(organization)
        update_data = organization_in.dict(skip_defaults=True)

        for field in organization_data:
            if field in update_data:
                setattr(organization, field, update_data[field])

        session.add(organization)
        await session.commit()
        await session.refresh(organization)

        return organization

    async def delete(
        self,
        session: AsyncSession,
        *,
        organization: Organization,
    ) -> None:
        session.delete(organization)
        await session.commit()

    async def set_first_contact_date(
        self,
        session: AsyncSession,
        *,
        organization: Organization,
        first_contact_date: date,
    ) -> Organization:
        organization.first_contact_date = first_contact_date
        session.add(organization)
        await session.commit()
        await session.refresh(organization)


crud_organization = CRUDOrganization()
