from typing import List
from app.models import Organization

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession


from app.api.providers import get_session, RoleChecker, get_current_user
from app.schemas.organization import (
    OrganizationOut,
    OrganizationCreate,
    OrganizationUpdate,
)
from app.crud.organization import crud_organization
from app.core.http_exceptions import (
    organization_already_exists_exception,
    organization_not_found_exception,
)

router = APIRouter()
admin_only = RoleChecker(["admin"])


@router.get("/", response_model=List[OrganizationOut])
async def get_organizations(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)
):
    """
    Get all organizations
    """
    organizations = await crud_organization.get_organizations(
        session, skip=skip, limit=limit
    )
    return organizations


@router.get("/{name}", response_model=OrganizationOut)
async def get_organization(name: str, session: AsyncSession = Depends(get_session)):
    """
    Get organization by name
    """
    organization = await crud_organization.get_by_name(session, name=name)
    if not organization:
        raise organization_not_found_exception

    return organization


@router.post("/", status_code=201, response_model=OrganizationOut)
async def create_organization(
    organization_in: OrganizationCreate,
    session: AsyncSession = Depends(get_session),
):
    """
    Create new organization
    """
    organization = await crud_organization.get_by_name(
        session, name=organization_in.name
    )
    if organization:
        raise organization_already_exists_exception

    organization = await crud_organization.create(
        session, organization_in=organization_in
    )

    return organization


@router.put("/{name}", status_code=201, response_model=OrganizationOut)
async def update_organization(
    name: str,
    organization_in: OrganizationUpdate,
    session: AsyncSession = Depends(get_session),
):
    """
    Update organization
    """
    organization = await crud_organization.get_by_name(session, name=name)
    if organization:
        raise organization_not_found_exception

    organization = await crud_organization.update(
        session, organization=organization, organization_in=organization_in
    )

    return organization


@router.delete("/{name}", status_code=204, dependencies=[Depends(admin_only)])
async def delete_organization(name: str, session: AsyncSession = Depends(get_session)):
    """
    Delete organization
    """
    organization = await crud_organization.get_by_name(session, name=name)
    if not organization:
        raise organization_not_found_exception

    crud_organization.delete(session, organization=organization)
