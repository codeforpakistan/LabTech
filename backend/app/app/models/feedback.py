from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User
    from .survey import Survey  # noqa: F401


class Feedback(Base):
    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="feedbacks")
    survey_id = Column(Integer, ForeignKey("survey.id"))
    survey = relationship("Survey", back_populates="feedbacks")
