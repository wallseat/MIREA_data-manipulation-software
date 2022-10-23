from typing import Optional

from datetime import date
from pydantic import BaseModel

class BaseTask(BaseModel):
    title: str
    description: Optional[str]
    priority_id: int
    type_id: int
    open_date: date
    due_date: Optional[date]
    author: str
    executor: str
    contract_id: Optional[int]
    contact_person_id: int

class CreateTask(BaseTask):
    pass

  
class Task(BaseTask):
    class Config:
        orm_mode = True
        
    id: int
    close_date: Optional[date]
    completed: bool