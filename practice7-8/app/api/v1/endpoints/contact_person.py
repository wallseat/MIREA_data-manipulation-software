from typing import List

from app.api.providers import RoleChecker, get_session
from app.core.http_exceptions import x_already_exists_exception, x_not_found_exception
from app.crud.contact_person import crud_contact_person
from app.crud.organization import crud_organization
from app.schemas.contact_person import (
    ContactPersonCreate,
    ContactPersonOut,
    ContactPersonUpdate,
)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
admin_only = RoleChecker(["admin"])

organization_not_found_exception = x_not_found_exception("Organization")
contact_person_already_exists_exception = x_already_exists_exception("Contact person")
contact_person_not_found_exception = x_not_found_exception("Contact person")


@router.get("/{organization}", response_model=List[ContactPersonOut])
async def get(
    organization: str,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
):
    """
    Get all contact persons by organization name
    """
    organization = await crud_organization.get_by_name(session, name=organization)
    if not organization:
        raise organization_not_found_exception

    contact_persons = await crud_contact_person.get(
        session, organization=organization, skip=skip, limit=limit
    )

    return contact_persons


@router.get("/", response_model=ContactPersonOut)
async def get_contact_person(
    first_name: str,
    second_name: str,
    email: str,
    session: AsyncSession = Depends(get_session),
):
    """
    Get contact person by first and second name
    """
    contact_persons = await crud_contact_person.get_by_first_second_name_email(
        session,
        first_name=first_name,
        second_name=second_name,
        email=email,
    )
    if not contact_persons:
        raise contact_person_not_found_exception

    return contact_persons


@router.post("/", status_code=201, response_model=ContactPersonOut)
async def create_contact_person(
    contact_person_in: ContactPersonCreate,
    session: AsyncSession = Depends(get_session),
):
    """
    Create new contact person
    """
    contact_person = await crud_contact_person.get_by_first_second_name_email(
        session,
        first_name=contact_person_in.first_name,
        second_name=contact_person_in.second_name,
        email=contact_person_in.email,
    )
    if contact_person:
        raise contact_person_already_exists_exception

    organization = await crud_organization.get_by_name(
        session, name=contact_person_in.organization_name
    )
    if not organization:
        raise organization_not_found_exception

    contact_person = await crud_contact_person.create(
        session, contact_person_in=contact_person_in, organization=organization
    )

    return contact_person


@router.put("/", status_code=201, response_model=ContactPersonOut)
async def update_organization(
    first_name: str,
    second_name: str,
    email: str,
    contact_person_in: ContactPersonUpdate,
    session: AsyncSession = Depends(get_session),
):
    """
    Update contact person
    """
    contact_person = await crud_contact_person.get_by_first_second_name_email(
        session,
        first_name=first_name,
        second_name=second_name,
        email=email,
    )
    if not contact_person:
        raise contact_person_not_found_exception

    if contact_person_in.organization_name:
        organization = await crud_organization.get_by_name(
            session,
            name=contact_person_in.organization_name,
        )
        if not organization:
            raise organization_not_found_exception

    contact_person = await crud_contact_person.update(
        session,
        contact_person=contact_person,
        contact_person_in=contact_person_in,
    )

    return contact_person


@router.delete("/", status_code=204, dependencies=[Depends(admin_only)])
async def delete_contact_person(
    first_name: str,
    second_name: str,
    email: str,
    session: AsyncSession = Depends(get_session),
):
    """
    Delete contact person
    """
    contact_person = await crud_contact_person.get_by_first_second_name_email(
        session,
        first_name=first_name,
        second_name=second_name,
        email=email,
    )
    if not contact_person:
        raise contact_person_not_found_exception

    crud_contact_person.delete(session, contact_person=contact_person)
