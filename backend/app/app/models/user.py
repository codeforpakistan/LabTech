from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item 
    from .hospital import Hospital  # noqa: F401
    from .department import Department
    from .survey import Survey
    from .feedback import Feedback


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    items = relationship("Item", back_populates="owner")
    hospitals = relationship("Hospital", back_populates="owner")
    surveys = relationship("Survey", back_populates="owner")
    feedbacks = relationship("Feedback", back_populates="owner")
    departments = relationship("Department", back_populates="owner")
    