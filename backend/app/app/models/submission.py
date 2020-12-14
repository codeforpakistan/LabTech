import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, JSON, Float, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User
    from .survey import Survey  # noqa: F401


class Submission(Base):
    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, index=True)
    answers = Column(JSON)
    images = Column(JSON)
    lat = Column(Float)
    lng = Column(Float)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="submissions")
    survey_id = Column(Integer, ForeignKey("survey.id"))
    survey = relationship("Survey", back_populates="submissions")
