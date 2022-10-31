from app.api.providers import get_current_user
from fastapi import APIRouter, Depends

from .endpoints import (
    contact_person,
    equipment,
    group,
    organization,
    user,
    contract,
    task,
    report,
)

v1_router = APIRouter()

v1_router.include_router(
    user.router,
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(get_current_user)],
)
v1_router.include_router(
    group.router,
    prefix="/group",
    tags=["group"],
    dependencies=[Depends(get_current_user)],
)
v1_router.include_router(
    organization.router,
    prefix="/organization",
    tags=["organization"],
    dependencies=[Depends(get_current_user)],
)
v1_router.include_router(
    contact_person.router,
    prefix="/contact_person",
    tags=["contact_person"],
    dependencies=[Depends(get_current_user)],
)
v1_router.include_router(
    equipment.router,
    prefix="/equipment",
    tags=["equipment"],
    dependencies=[Depends(get_current_user)],
)
v1_router.include_router(
    contract.router,
    prefix="/contract",
    tags=["contract"],
    dependencies=[Depends(get_current_user)],
)
v1_router.include_router(
    task.router,
    prefix="/task",
    tags=["task"],
    dependencies=[Depends(get_current_user)],
)
v1_router.include_router(
    report.router,
    prefix="/report",
    tags=["report"],
    dependencies=[Depends(get_current_user)],
)

__all__ = ["v1_router"]
