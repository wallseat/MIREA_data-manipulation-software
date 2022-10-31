from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.providers import RoleChecker, get_session
from app.core.http_exceptions import (
    x_not_found_exception,
)
from app.schemas.report import ReportOut, ReportCreate
from app.crud.user import crud_user
from app.crud.task import crud_task

router = APIRouter()

admin_manager_only = RoleChecker(["admin", "manager"])

user_nf = x_not_found_exception("User")


@router.get(
    "/",
    response_model=ReportOut,
    dependencies=[Depends(admin_manager_only)],
)
async def get_report(
    user_name: str,
    start_date: date,
    end_date: date = date.today(),
    session: AsyncSession = Depends(get_session),
):
    user = await crud_user.get_by_name(session, name=user_name)
    if not user:
        raise user_nf

    tasks = await crud_task.get_by_id_and_date_period(
        session,
        user=user,
        start_date=start_date,
        end_date=end_date,
    )

    completed_task_count = 0
    completed_out_of_date_task_count = 0
    not_completed_task_count = 0
    not_completed_out_of_date_task_count = 0

    for task in tasks:
        if task.completed:
            if task.close_date <= task.due_date:
                completed_task_count += 1
            else:
                completed_out_of_date_task_count += 1
        else:
            if task.due_date >= date.today():
                not_completed_task_count += 1
            else:
                not_completed_out_of_date_task_count += 1

    return ReportOut(
        user=user.name,
        start_date=start_date,
        end_date=end_date,
        task_count=len(tasks),
        completed_task_count=completed_task_count,
        completed_out_of_date_task_count=completed_out_of_date_task_count,
        not_completed_task_count=not_completed_task_count,
        not_completed_out_of_date_task_count=not_completed_out_of_date_task_count,
    )
