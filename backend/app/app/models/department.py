from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User
    from .hospital import Hospital
    from .survey import Survey  # noqa: F401


class Department(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="departments")
    hospital_id = Column(Integer, ForeignKey("hospital.id"))
    hospital = relationship("Hospital", back_populates="departments")
    surveys = relationship("Survey", back_populates="department")
