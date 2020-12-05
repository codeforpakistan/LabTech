from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User
    from .hospital import Hospital  # noqa: F401


class Survey(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="surveys")
    hospital_id = Column(Integer, ForeignKey("hospital.id"))
    hospital = relationship("Hospital", back_populates="surveys")
