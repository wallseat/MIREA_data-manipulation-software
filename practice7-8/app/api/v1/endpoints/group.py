from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.providers import get_session, RoleChecker
from app.schemas.group import GroupOut, GroupAddUsers
from app.schemas.user import UserOut
from app.crud.user import crud_user
from app.crud.group import crud_group
from app.core.http_exceptions import (
    x_not_found_exception_factory,
    x_already_exists_exception_factory,
)

router = APIRouter()

admin_only = RoleChecker(["admin"])

group_already_exists_exception = x_already_exists_exception_factory("Group")
group_not_found_exception = x_not_found_exception_factory("Group")


@router.get("/", response_model=List[GroupOut], dependencies=[Depends(admin_only)])
async def get_groups(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)
):
    """
    Get all groups
    """
    groups = await crud_group.get_groups(session, skip=skip, limit=limit)
    return groups


@router.get(
    "/users/{group_name}",
    response_model=List[UserOut],
    dependencies=[Depends(admin_only)],
    tags=["user"],
)
async def get_user_by_group(
    group_name: str, *, session: AsyncSession = Depends(get_session)
):
    """
    Get users by group
    """
    db_obj = await crud_group.get_by_name(session, name=group_name)
    if not db_obj:
        raise group_not_found_exception

    users = await crud_user.get_by_group(session, group_name=group_name)
    return users


@router.post(
    "/users/{group_name}",
    status_code=201,
    response_model=List[UserOut],
    dependencies=[Depends(admin_only)],
    tags=["user"],
)
async def add_user_to_group(
    group_name: str,
    group_add_users_in: GroupAddUsers,
    session: AsyncSession = Depends(get_session),
):
    """
    Add users to group
    """
    group = await crud_group.get_by_name(session, name=group_name)
    if not group:
        raise group_not_found_exception

    users = []
    for username in group_add_users_in.usernames:
        db_obj = await crud_user.get_by_name(session, name=username)
        if not db_obj:
            raise user_not_found_exception
        users.append(db_obj)

    await crud_group.add_users_to_group(
        session, users_ids=[user.id for user in users], group_id=group.id
    )

    return users


@router.delete(
    "/users/{group_name}",
    response_model=List[UserOut],
    dependencies=[Depends(admin_only)],
    tags=["user"],
)
async def remove_users_from_group(
    group_name: str,
    group_add_users_in: GroupAddUsers,
    session: AsyncSession = Depends(get_session),
):
    """
    Remove users from group
    """
    group = await crud_group.get_by_name(session, name=group_name)
    if not group:
        raise group_not_found_exception

    users = []
    for username in group_add_users_in.usernames:
        db_obj = await crud_user.get_by_name(session, name=username)
        if not db_obj:
            raise user_not_found_exception
        users.append(db_obj)

    await crud_group.remove_users_from_group(
        session, users_ids=[user.id for user in users], group_id=group.id
    )

    return users
