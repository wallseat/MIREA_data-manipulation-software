from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.providers import get_session, RoleChecker, get_current_user
from app.schemas.user import UserOut, UserCreate, UserUpdatePassword, UserUpdateName
from app.models import User
from app.crud.user import crud_user
from app.core.security import verify_password
from app.core.http_exceptions import (
    permission_denied_exception,
    x_already_exists_exception_factory,
    x_not_found_exception_factory,
    credentials_exception,
)

router = APIRouter()

admin_only = RoleChecker(["admin"])
is_admin = RoleChecker(["admin"], raise_not_allowed=False)

user_not_found_exception = x_not_found_exception_factory("User")
user_already_exists_exception = x_already_exists_exception_factory("User")


@router.post(
    "/",
    response_model=UserOut,
    status_code=201,
    dependencies=[Depends(admin_only)],
)
async def create_user(
    user_in: UserCreate, *, session: AsyncSession = Depends(get_session)
):
    """
    Register new user
    """

    user = await crud_user.get_by_name(session, name=user_in.name)
    if user:
        raise user_already_exists_exception

    user = await crud_user.create(session, user_in=user_in)

    return user


@router.get("/{username}", response_model=UserOut)
async def get_user_by_name(
    username: str, *, session: AsyncSession = Depends(get_session)
):
    """
    Get user by id
    """

    user_obj = await crud_user.get_by_name(session, name=username)
    if not user_obj:
        raise user_not_found_exception

    return user_obj


@router.put("/change/password", status_code=201, response_model=UserOut)
async def change_user_password(
    username: str,
    user_update_password_in: UserUpdatePassword,
    *,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    have_permission: bool = Depends(is_admin)
):
    """
    Change user password
    """
    if current_user.name != username and not have_permission:
        raise permission_denied_exception

    user_obj = await crud_user.get_by_name(session, name=username)
    if not user_obj:
        raise user_not_found_exception

    if not verify_password(
        user_update_password_in.old_password, user_obj.password_hash
    ):
        raise credentials_exception

    user_obj = await crud_user.update_password(
        session, user_obj=user_obj, new_password=user_update_password_in.new_password
    )

    return user_obj


@router.put("/change/name", status_code=201, response_model=UserOut)
async def change_user_password(
    username: str,
    user_update_name_in: UserUpdateName,
    *,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    have_permission: bool = Depends(is_admin)
):
    """
    Change user name
    """

    if current_user.name != username and not have_permission:
        raise permission_denied_exception

    user_obj = await crud_user.get_by_name(session, name=username)
    if not user_obj:
        raise user_not_found_exception

    user_obj = await crud_user.update_name(
        session, user_obj=user_obj, new_name=user_update_name_in.name
    )

    return user_obj
