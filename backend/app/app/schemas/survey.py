from typing import Optional

from pydantic import BaseModel


# Shared properties
class SurveyBase(BaseModel):
    name: Optional[str] = None


# Properties to receive on item creation
class SurveyCreate(SurveyBase):
    name: str
    hospital_id: int



# Properties to receive on item update
class SurveyUpdate(SurveyBase):
    pass


# Properties shared by models stored in DB
class SurveyInDBBase(SurveyBase):
    id: int
    name: str
    owner_id: int
    hospital_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Survey(SurveyInDBBase):
    pass


# Properties properties stored in DB
class SurveyInDB(SurveyInDBBase):
    pass
