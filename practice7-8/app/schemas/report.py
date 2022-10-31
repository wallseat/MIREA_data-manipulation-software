from typing import Optional
from datetime import date

from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    user: str
    date_start: date
    date_end: Optional[date] = Field(default_factory=date.today)


class ReportOut(BaseModel):
    user: str
    start_date: date
    end_date: date
    task_count: int
    completed_task_count: int
    completed_out_of_date_task_count: int
    not_completed_task_count: int
    not_completed_out_of_date_task_count: int