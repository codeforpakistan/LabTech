import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, JSON, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User # noqa: F401
    from .department import Department
    from .submission import Submission


class Survey(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    questions = Column(JSON)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="surveys")
    department_id = Column(Integer, ForeignKey("department.id"))
    department = relationship("Department", back_populates="surveys")
    submissions = relationship("Submission", back_populates="survey")
