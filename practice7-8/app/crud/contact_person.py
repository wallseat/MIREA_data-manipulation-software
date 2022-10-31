from uuid import UUID
from typing import List, Optional

from app.models import ContactPerson, Organization
from app.schemas.contact_person import ContactPersonCreate, ContactPersonUpdate
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDContactPerson:
    async def get(
        self,
        session: AsyncSession,
        *,
        organization: Organization,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Organization]:
        result = await session.execute(
            select(ContactPerson)
            .offset(skip)
            .limit(limit)
            .where(ContactPerson.organization_id == organization.id)
        )

        return result.scalars().all()

    async def get_by_id(
        self, session: AsyncSession, *, id_: UUID
    ) -> Optional[ContactPerson]:
        result = await session.execute(
            select(ContactPerson).where(ContactPerson.id == id_)
        )

        return result.scalars().first()

    async def get_by_first_second_name_email(
        self,
        session: AsyncSession,
        *,
        first_name: str,
        second_name: str,
        email: str,
    ) -> Optional[Organization]:
        result = await session.execute(
            select(ContactPerson).where(
                and_(
                    ContactPerson.first_name == first_name,
                    ContactPerson.second_name == second_name,
                    ContactPerson.email == email,
                )
            )
        )

        return result.scalars().first()

    async def create(
        self,
        session: AsyncSession,
        *,
        contact_person_in: ContactPersonCreate,
        organization: Organization,
    ) -> ContactPerson:

        organization = ContactPerson(
            **contact_person_in.dict(exclude=["organization_name"]),
            organization_id=organization.id,
        )
        session.add(organization)

        await session.commit()
        await session.refresh(organization)

        return organization

    async def update(
        self,
        session: AsyncSession,
        *,
        contact_person: ContactPerson,
        contact_person_in: ContactPersonUpdate,
        organization: Optional[Organization] = None,
    ) -> ContactPerson:

        contact_person_data = jsonable_encoder(contact_person)
        update_data = contact_person_in.dict(skip_defaults=True)

        if organization:
            contact_person.organization_id = organization.id

        for field in contact_person_data:
            if field == "organization_name":
                continue

            if field in update_data:
                setattr(contact_person, field, update_data[field])

        session.add(contact_person)
        await session.commit()
        await session.refresh(contact_person)

        return contact_person

    async def delete(
        self,
        session: AsyncSession,
        *,
        contact_person: ContactPerson,
    ) -> None:
        session.delete(contact_person)
        await session.commit()


crud_contact_person = CRUDContactPerson()
