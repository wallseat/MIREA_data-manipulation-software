from uuid import UUID
from typing import Optional, List

from sqlalchemy import select, join
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, UserGroup, Group
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


class CRUDUser:
    async def get_by_name(self, session: AsyncSession, *, name: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.name == name))

        return result.scalars().first()

    async def get_by_group(
        self, session: AsyncSession, *, group_name: str
    ) -> List[User]:
        result = await session.execute(
            select(User)
            .select_from(
                join(User, UserGroup, User.id == UserGroup.user_id, isouter=True).join(
                    Group, UserGroup.group_id == Group.id, isouter=True
                )
            )
            .where(Group.name == group_name)
        )

        return result.scalars().all()

    async def create(self, session: AsyncSession, *, user_in: UserCreate) -> User:
        
        password_hash = get_password_hash(user_in.password)

        user = User(name=user_in.name, password_hash=password_hash)

        session.add(user)

        await session.commit()
        await session.refresh(user)

        return user

    async def update_password(
        self, session: AsyncSession, *, user_obj: User, new_password: str
    ) -> User:

        user_obj.password_hash = get_password_hash(new_password)

        session.add(user_obj)

        await session.commit()
        await session.refresh(user_obj)

        return user_obj

    async def update_name(
        self, session: AsyncSession, *, user_obj: User, new_name: str
    ) -> User:

        user_obj.name = new_name

        session.add(user_obj)

        await session.commit()
        await session.refresh(user_obj)

        return user_obj


crud_user = CRUDUser()
