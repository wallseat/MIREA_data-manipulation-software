from datetime import date

from pydantic import BaseModel


class ReportOut(BaseModel):
    user: str
    start_date: date
    end_date: date
    task_count: int
    completed_task_count: int
    completed_out_of_date_task_count: int
    not_completed_task_count: int
    not_completed_out_of_date_task_count: int
