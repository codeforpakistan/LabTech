from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, JSON
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User # noqa: F401
    from .department import Department
    from .feedback import Feedback # noqa: F401


class Survey(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    answers = Column(JSON)
    images = Column(JSON)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="surveys")
    department_id = Column(Integer, ForeignKey("department.id"))
    department = relationship("Department", back_populates="surveys")
    feedbacks = relationship("Feedback", back_populates="survey")
