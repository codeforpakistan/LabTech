from typing import Optional
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class DepartmentBase(BaseModel):
    name: Optional[str] = None


# Properties to receive on department creation
class DepartmentCreate(DepartmentBase):
    name: str
    hospital_id: int


# Properties to receive on department update
class DepartmentUpdate(DepartmentBase):
    pass


# Properties shared by models stored in DB
class DepartmentInDBBase(DepartmentBase):
    id: int
    name: str
    owner_id: int
    # hospital: str
    hospital_id: int
    created_date: datetime


    class Config:
        orm_mode = True


# Properties to return to client
class Department(DepartmentInDBBase):
    pass


# Properties properties stored in DB
class DepartmentInDB(DepartmentInDBBase):
    pass
