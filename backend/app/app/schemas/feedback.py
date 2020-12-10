from typing import Optional

from pydantic import BaseModel


# Shared properties
class FeedbackBase(BaseModel):
    comment: Optional[str] = None


# Properties to receive on feedback creation
class FeedbackCreate(FeedbackBase):
    comment: str


# Properties to receive on feedback update
class FeedbackUpdate(FeedbackBase):
    pass


# Properties shared by models stored in DB
class FeedbackInDBBase(FeedbackBase):
    id: int
    comment: str

    class Config:
        orm_mode = True


# Properties to return to client
class Feedback(FeedbackInDBBase):
    pass


# Properties properties stored in DB
class FeedbackInDB(FeedbackInDBBase):
    pass
