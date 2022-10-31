from uuid import UUID
from typing import List

from app.api.providers import RoleChecker, get_session, get_current_user
from app.core.http_exceptions import (
    x_already_exists_exception,
    x_not_found_exception,
    permission_denied_exception,
)
from app.crud.task import crud_task
from app.crud.user import crud_user
from app.crud.contact_person import crud_contact_person
from app.models import User
from app.schemas.task import (
    TaskCreate,
    TaskPriorityCreate,
    TaskPriorityOut,
    TaskUpdate,
    TaskOut,
    TaskTypeOut,
    TaskTypeCreate,
)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

admin_only = RoleChecker(["admin"])
admin_manager_only = admin_only.extend(["manager"])
is_admin = RoleChecker(["admin"], raise_not_allowed=False)

priority_nf = x_not_found_exception("Task priority")
type_nf = x_not_found_exception("Task type")
user_nf = x_not_found_exception("User")
task_nf = x_not_found_exception("Task")
contact_person_nf = x_not_found_exception("Contact person")

task_type_ae = x_already_exists_exception("Task type")
task_priority_ae = x_already_exists_exception("Task priority")


@router.get(
    "/",
    response_model=List[TaskOut],
)
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    tasks = await crud_task.get(session, user=current_user, skip=skip, limit=limit)

    return tasks


@router.post(
    "/",
    status_code=201,
    response_model=TaskOut,
    dependencies=[Depends(admin_manager_only)],
)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    priority = await crud_task.get_priority(session, priority=task_in.priority)
    if not priority:
        raise priority_nf

    type_ = await crud_task.get_type(session, task_type=task_in.type_)
    if not type_:
        raise type_nf

    contact_person = await crud_contact_person.get_by_id(
        session, id_=task_in.contact_person_id
    )
    if not contact_person:
        raise contact_person_nf

    executor = await crud_user.get_by_name(session, name=task_in.executor_name)
    if not executor:
        raise user_nf

    task = await crud_task.create(
        session,
        user=current_user,
        task_in=task_in,
        executor=executor,
        type_=type_,
        priority=priority,
    )

    return task


@router.put(
    "/{id}",
    status_code=201,
    response_model=TaskOut,
    dependencies=[Depends(admin_manager_only)],
)
async def update_task(
    id: UUID,
    task_in: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    is_admin: bool = Depends(is_admin),
):
    task = await crud_task.get_by_id(session, id=id)
    if not task:
        raise task_nf

    if task.executor_id != current_user.id and not is_admin:
        raise permission_denied_exception

    priority = None
    if task_in.priority:
        priority = await crud_task.get_priority(session, priority=task_in.priority)
        if not priority:
            raise priority_nf

    type_ = None
    if task_in.type_:
        type_ = await crud_task.get_type(session, task_type=task_in.type_)
        if not type_:
            raise type_nf

    executor = None
    if task_in.executor_name:
        executor = await crud_user.get_by_name(session, name=task_in.executor_name)
        if not executor:
            raise user_nf

    task = await crud_task.update(
        session,
        user=current_user,
        task_in=task_in,
        executor=executor,
        type_=type_,
        priority=priority,
    )

    return task


@router.delete(
    "/{id}",
    status_code=204,
    dependencies=[Depends(admin_only)],
)
async def delete_task(
    id: UUID,
    session: AsyncSession = Depends(get_session),
):
    task = await crud_task.get_by_id(session, id=id)
    if not task:
        raise task_nf

    await crud_task.delete(session, task=task)


@router.get("/type/", response_model=List[TaskTypeOut])
async def get_task_types(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
):
    return await crud_task.get_types(session, skip=skip, limit=limit)


@router.post(
    "/type/",
    response_model=TaskTypeOut,
    dependencies=[Depends(admin_only)],
)
async def create_task_type(
    task_type_in: TaskTypeCreate,
    session: AsyncSession = Depends(get_session),
):
    task_type = await crud_task.get_type(session, task_type=task_type_in.type_)
    if task_type:
        raise task_type_ae

    task_type = await crud_task.create_type(session, task_type_in=task_type_in)

    return task_type


@router.delete(
    "/type/{type_}",
    status_code=204,
    dependencies=[Depends(admin_only)],
)
async def delete_task_type(
    type_: str,
    session: AsyncSession = Depends(get_session),
):
    task_type = await crud_task.get_type(session, task_type=type_)
    if not task_type:
        raise type_nf

    await crud_task.delete_type(session, task_type=task_type)


@router.get("/priority/", response_model=List[TaskPriorityOut])
async def get_task_priorities(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
):
    return await crud_task.get_priorities(session, skip=skip, limit=limit)


@router.post(
    "/priority/",
    response_model=TaskPriorityOut,
    dependencies=[Depends(admin_only)],
)
async def create_task_priority(
    task_priority_in: TaskPriorityCreate,
    session: AsyncSession = Depends(get_session),
):
    task_priority = await crud_task.get_priority(
        session, priority=task_priority_in.priority
    )
    if task_priority:
        raise task_priority_ae

    task_type = await crud_task.create_priority(
        session, task_priority_in=task_priority_in
    )

    return task_type


@router.delete(
    "/priority/{priority}",
    status_code=204,
    dependencies=[Depends(admin_only)],
)
async def delete_task_priority(
    priority: str,
    session: AsyncSession = Depends(get_session),
):
    task_priority = await crud_task.get_priority(session, priority=priority)
    if not task_priority:
        raise priority_nf

    await crud_task.delete_priority(session, task_priority=task_priority)
