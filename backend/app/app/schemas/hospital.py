from typing import Optional, Dict, Any
from datetime import datetime

from pydantic import BaseModel
from .user import UserInDB


# Shared properties
class HospitalBase(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    hospital_type: Optional[str] = None
    lat: Optional[float] = 0.0
    lng: Optional[float] = 0.0


# Properties to receive on hospital creation
class HospitalCreate(HospitalBase):
    name: str
    address: str
    hospital_type: str
    lat: float
    lng: float


# Properties to receive on hospital update
class HospitalUpdate(HospitalBase):
    pass


# Properties shared by models stored in DB
class HospitalInDBBase(HospitalBase):
    id: int
    name: str
    address: str
    # Because it is already inheriting validation from HospitalBase
    # hospital_type: str
    lat: float
    lng: float
    owner_id: int
    owner: UserInDB
    departments: list
    created_date: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Hospital(HospitalInDBBase):
    pass


# Properties properties stored in DB
class HospitalInDB(HospitalInDBBase):
    pass
