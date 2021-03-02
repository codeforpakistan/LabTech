import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User
    from .department import Department
    from .survey import Survey # noqa: F401


class Hospital(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    hospital_type = Column(String, index=True)
    address = Column(String, index=True)
    lat = Column(Float)
    lng = Column(Float)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="hospitals")
    departments = relationship("Department", back_populates="hospital")
