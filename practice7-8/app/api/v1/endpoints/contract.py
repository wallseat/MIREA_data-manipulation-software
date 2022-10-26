from datetime import date
from typing import List
from uuid import UUID

from app.api.providers import RoleChecker, get_session
from app.core.http_exceptions import x_already_exists_exception, x_not_found_exception
from app.crud.contract import crud_contract
from app.crud.organization import crud_organization
from app.schemas.contract import (
    ContractCreate,
    ContractOut,
    ContractTypeCreate,
    ContractTypeOut,
    ContractTypeUpdate,
    ContractUpdate,
)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
admin_only = RoleChecker(["admin"])

organization_not_found_exception = x_not_found_exception("Organization")

contract_not_found_exception = x_not_found_exception("Contract")
contract_already_exists_exception = x_already_exists_exception("Contract")

contract_type_not_found_exception = x_not_found_exception("Contract type")
contract_type_already_exists_exception = x_already_exists_exception("Contract type")


@router.get("/", response_model=List[ContractOut])
async def get_contracts_by_organization_name(
    organization_name: str = "",
    limit: int = 0,
    skip: int = 100,
    session: AsyncSession = Depends(get_session),
):
    """
    Get all contract or by organization name
    """
    organization = None
    if organization_name:
        organization = await crud_organization.get_by_name(
            session, name=organization_name
        )
        if not organization:
            raise organization_not_found_exception

    contracts = await crud_contract.get(
        session,
        organization_id=organization.id if organization else None,
        limit=limit,
        skip=skip,
    )

    return contracts


@router.get("/{contract_id}", response_model=ContractOut)
async def get_contract_by_id(
    contract_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """
    Get contract by id
    """

    contract = await crud_contract.get_by_id(session, contract_id=contract_id)
    if not contract:
        raise contract_not_found_exception

    return contract


@router.post("/", response_model=ContractOut)
async def create_contract(
    contract_in: ContractCreate,
    session: AsyncSession = Depends(get_session),
):
    """
    Create new contract
    """

    organization = await crud_organization.get_by_name(
        session, name=contract_in.organization_name
    )
    if not organization:
        raise organization_not_found_exception

    type_ = await crud_contract.get_type(session, type_=contract_in.type_)
    if not type_:
        raise contract_type_not_found_exception

    contract = await crud_contract.create(
        session,
        contract_in=contract_in,
        organization_id=organization.id,
        type_id=type_.id,
    )

    if not organization.first_contract_date:
        organization = await crud_organization.set_first_contact_date(
            session, organization=organization, date=date.today()
        )

    return contract


@router.put("/{contract_id}", response_model=ContractOut)
async def update_contract(
    contract_id: UUID,
    contract_in: ContractUpdate,
    session: AsyncSession = Depends(get_session),
):
    """
    Update contract
    """

    contract = await crud_contract.get_by_id(session, contract_id=contract_id)
    if not contract:
        raise contract_not_found_exception

    contract = await crud_contract.update(
        session, contract=contract, contract_in=contract_in
    )

    return contract


@router.delete("/{contract_id}", status_code=204, dependencies=[Depends(admin_only)])
async def delete_contract(
    contract_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    contract = await crud_contract.get_by_id(session, contract_id=contract_id)
    if not contract:
        raise contract_not_found_exception

    await crud_contract.delete(session, contract=contract)


@router.get("/type", response_model=List[ContractTypeOut])
async def get_contract_types(
    limit: int = 0,
    skip: int = 100,
    session: AsyncSession = Depends(get_session),
):
    """
    Get all contract types
    """
    types = await crud_contract.get_types(session, limit=limit, skip=skip)

    return types


@router.post(
    "/type",
    response_model=ContractTypeOut,
    dependencies=[Depends(admin_only)],
)
async def create_contract_type(
    contract_type_in: ContractTypeCreate,
    session: AsyncSession = Depends(get_session),
):
    """
    Create new contract type
    """
    type_ = await crud_contract.get_type(session, type_=contract_type_in.type_)
    if type_:
        raise contract_type_already_exists_exception

    type_ = await crud_contract.create_type(session, contract_type_in=contract_type_in)

    return type_


@router.put(
    "/type/{type_}",
    response_model=ContractTypeOut,
    dependencies=[Depends(admin_only)],
)
async def create_contract_type(
    type_: str,
    contract_type_in: ContractTypeUpdate,
    session: AsyncSession = Depends(get_session),
):
    """
    Update contract type
    """
    type_obj = await crud_contract.get_type(session, type_=type_)
    if not type_obj:
        raise contract_type_not_found_exception

    type_obj = await crud_contract.update_type(
        session, type_=type_obj, contract_type_in=contract_type_in
    )

    return type_obj


@router.delete(
    "/type/{type_}",
    response_model=ContractTypeOut,
    dependencies=[Depends(admin_only)],
)
async def delete_contract_types(
    type_: str,
    session: AsyncSession = Depends(get_session),
):
    """
    Delete contract type
    """
    type_obj = await crud_contract.get_type(session, type_=type_)
    if not type_obj:
        raise contract_type_not_found_exception

    await crud_contract.delete_type(session, type_=type_obj)
