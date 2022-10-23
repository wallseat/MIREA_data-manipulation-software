from uuid import UUID

from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    
class UserCreate(UserBase):
    password: str

class UserUpdatePassword(BaseModel):
    old_password: str
    new_password: str

class UserUpdateName(UserBase):
    pass

class UserOut(UserBase):
    class Config:
        orm_mode = True
    
    id: UUID