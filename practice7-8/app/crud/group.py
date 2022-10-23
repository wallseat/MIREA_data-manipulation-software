from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from app.models import Group, UserGroup


class CRUDGroup:
    async def get_groups(self, session: AsyncSession, skip: int = 0, limit: int = 100):
        result = await session.execute(select(Group).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_name(self, session: AsyncSession, *, name: str) -> Optional[Group]:
        result = await session.execute(select(Group).where(Group.name == name))
        return result.scalars().first()

    async def add_users_to_group(
        self, session: AsyncSession, *, users_ids: List[UUID], group_id: UUID
    ):
        await session.execute(
            insert(UserGroup)
            .values(
                [{"user_id": user_id, "group_id": group_id} for user_id in users_ids]
            )
            .on_conflict_do_nothing()
        )

        await session.commit()

    async def remove_users_from_group(
        self, session: AsyncSession, *, users_ids: List[UUID], group_id: UUID
    ):
        await session.execute(
            delete(UserGroup).where(
                and_(UserGroup.group_id == group_id, UserGroup.user_id.in_(users_ids))
            )
        )

        await session.commit()


crud_group = CRUDGroup()
