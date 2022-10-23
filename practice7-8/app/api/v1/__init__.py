from app.api.v1.endpoints import organization
from fastapi import APIRouter, Depends

from app.api.providers import get_current_user

from .endpoints import user, group, organization, contact_person


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

__all__ = ["v1_router"]
