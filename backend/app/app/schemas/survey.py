from typing import Optional

from pydantic import BaseModel


# Shared properties
class SurveyBase(BaseModel):
    name: Optional[str] = None
    answers: Optional[list] = None
    images: Optional[list] = None


# Properties to receive on item creation
class SurveyCreate(SurveyBase):
    name: str
    answers: list
    images: list
    department_id: int



# Properties to receive on item update
class SurveyUpdate(SurveyBase):
    pass


# Properties shared by models stored in DB
class SurveyInDBBase(SurveyBase):
    id: int
    name: str
    answers: list
    images: list
    owner_id: int
    department: str
    department_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Survey(SurveyInDBBase):
    pass


# Properties properties stored in DB
class SurveyInDB(SurveyInDBBase):
    pass
