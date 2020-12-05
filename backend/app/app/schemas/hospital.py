from typing import Optional

from pydantic import BaseModel


# Shared properties
class HospitalBase(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None


# Properties to receive on hospital creation
class HospitalCreate(HospitalBase):
    name: str
    address: str


# Properties to receive on hospital update
class HospitalUpdate(HospitalBase):
    pass


# Properties shared by models stored in DB
class HospitalInDBBase(HospitalBase):
    id: int
    name: str
    address: str
    owner_id: int
    departments: list

    class Config:
        orm_mode = True


# Properties to return to client
class Hospital(HospitalInDBBase):
    pass


# Properties properties stored in DB
class HospitalInDB(HospitalInDBBase):
    pass
