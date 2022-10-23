from typing import AsyncGenerator, List

from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, join

from app.core.const import ALGORITHM, SECRET_KEY
from app.core.security import oauth2_scheme
from app.core.http_exceptions import (
    credentials_exception,
    x_not_found_exception_factory,
    permission_denied_exception,
)
from app.crud.user import crud_user
from app.db import engine
from app.models import User, UserGroup, Group

user_not_found_exception = x_not_found_exception_factory("User")


async def get_session() -> AsyncGenerator:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)
) -> User:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    db_obj = await crud_user.get_by_name(db, name=username)

    if db_obj is None:
        raise user_not_found_exception

    return db_obj


class RoleChecker:
    def __init__(self, allowed_groups: List[str], *, raise_not_allowed: bool = True):
        self.allowed_groups = allowed_groups
        self.raise_not_allowed = raise_not_allowed

    async def __call__(
        self,
        *,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
    ) -> bool:
        result = await session.execute(
            select(Group.name)
            .select_from(
                join(User, UserGroup, UserGroup.user_id == User.id, isouter=True).join(
                    Group,
                    UserGroup.group_id == Group.id,
                    isouter=True,
                ),
            )
            .where(User.id == user.id)
        )

        groups = result.scalars().all()

        intersected_groups = set(self.allowed_groups).intersection(set(groups))

        if not intersected_groups and self.raise_not_allowed:
            raise permission_denied_exception

        return bool(intersected_groups)
