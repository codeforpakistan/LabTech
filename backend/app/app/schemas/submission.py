from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from typing import List, Dict


# Shared properties
class SubmissionBase(BaseModel):
    comment: Optional[str] = ''
    answers: Optional[List[Dict]] = []
    images: Optional[List[str]] = []
    lat: Optional[float] = 0.0
    lng: Optional[float] = 0.0


# Properties to receive on submission creation
class SubmissionCreate(SubmissionBase):
    comment: str
    answers: List[Dict]
    images: List[str]
    lat: float
    lng: float
    survey_id: int


# Properties to receive on submission update
class SubmissionUpdate(SubmissionBase):
    pass


# Properties shared by models stored in DB
class SubmissionInDBBase(SubmissionBase):
    id: int
    comment: str
    answers: List[Dict]
    images: List[str]
    lat: float
    lng: float
    owner_id: int
    survey_id: int
    hospital: Optional[str] = ''
    department: Optional[str] = ''
    created_date: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Submission(SubmissionInDBBase):
    pass


# Properties properties stored in DB
class SubmissionInDB(SubmissionInDBBase):
    pass
