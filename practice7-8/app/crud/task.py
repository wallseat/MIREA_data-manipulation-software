from uuid import UUID
from typing import Optional, List
from datetime import date

from sqlalchemy import select, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from fastapi.encoders import jsonable_encoder

from app.models import Task, User, TaskType, TaskPriority
from app.schemas.task import TaskCreate, TaskPriorityCreate, TaskTypeCreate, TaskUpdate


class CRUDTask:
    async def get(
        self, session: AsyncSession, *, user: User, skip: int = 0, limit: int = 100
    ) -> Optional[Task]:
        stmt = (
            select(Task)
            .where(or_(Task.executor_id == user.id, Task.author_id == user.id))
            .offset(skip)
            .limit(limit)
        )

        result = await session.execute(stmt)

        return result.scalars().all()

    async def get_by_id(self, session: AsyncSession, *, id: UUID) -> Optional[Task]:
        stmt = select(Task).where(Task.id == id)

        result = await session.execute(stmt)

        return result.scalars().first()

    async def get_by_id_and_date_period(
        self, session: AsyncSession, *, user: User, start_date: date, end_date: date
    ) -> List[Task]:
        stmt = select(Task).where(
            and_(
                Task.executor_id == user.id,
                Task.open_date >= start_date,
                Task.open_date <= end_date,
            )
        )

        result = await session.execute(stmt)

        return result.scalars().all()

    async def create(
        self,
        session: AsyncSession,
        *,
        user: User,
        task_in: TaskCreate,
        executor: User,
        type_: TaskType,
        priority: TaskPriority,
    ) -> Task:

        data = task_in.dict()

        data["author_id"] = user.id
        data["executor_id"] = executor.id
        data["type_id"] = type_.id
        data["priority_id"] = priority.id
        data["open_date"] = date.today()

        task = Task(**data)
        session.add(task)

        await session.commit()
        await session.refresh(task)

        return task

    async def update(
        self,
        session: AsyncSession,
        *,
        task: Task,
        task_in: TaskUpdate,
        executor: Optional[User] = None,
        type_: Optional[TaskType] = None,
        priority: Optional[TaskPriority] = None,
    ) -> Task:
        data = jsonable_encoder(task)

        update_data = task_in.dict(exclude_unset=True)
        if executor:
            update_data["executor_id"] = executor.id
        if type_:
            update_data["type_id"] = type_.id
        if priority:
            update_data["priority_id"] = priority.id

        for field in data:
            if field in update_data:
                setattr(task, field, update_data[field])

        await session.commit()
        await session.refresh(task)

        return task

    async def delete(self, session: AsyncSession, *, task: Task) -> None:
        session.delete(task)
        await session.commit()

    async def get_types(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[TaskType]:
        stmt = select(TaskType).offset(skip).limit(limit)

        result = await session.execute(stmt)

        return result.scalars().all()

    async def get_type(
        self, session: AsyncSession, *, task_type: str
    ) -> Optional[TaskType]:
        stmt = select(TaskType).where(TaskType.type == task_type)

        result = await session.execute(stmt)

        return result.scalars().first()

    async def create_type(
        self, session: AsyncSession, *, task_type_in: TaskTypeCreate
    ) -> TaskType:

        task_type = TaskType(type=task_type_in.type_)

        session.add(task_type)

        await session.commit()
        await session.refresh(task_type)

        return task_type

    async def delete_type(self, session: AsyncSession, *, task_type: TaskType) -> None:
        session.delete(task_type)
        await session.commit()

    async def get_priorities(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[TaskPriority]:

        stmt = select(TaskPriority).offset(skip).limit(limit)

        result = await session.execute(stmt)

        return result.scalars().all()

    async def get_priority(
        self, session: AsyncSession, *, priority: str
    ) -> Optional[TaskPriority]:
        stmt = select(TaskPriority).where(TaskPriority.priority == priority)

        result = await session.execute(stmt)

        return result.scalars().first()

    async def create_priority(
        self, session: AsyncSession, *, task_priority_in: TaskPriorityCreate
    ) -> TaskPriority:

        task_priority = TaskPriority(priority=task_priority_in.priority)

        session.add(task_priority)

        await session.commit()
        await session.refresh(task_priority)

        return task_priority

    async def delete_priority(
        self, session: AsyncSession, *, task_priority: TaskPriority
    ) -> None:
        session.delete(task_priority)
        await session.commit()


crud_task = CRUDTask()
