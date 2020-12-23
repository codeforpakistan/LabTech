from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate


class CRUDDepartment(CRUDBase[Department, DepartmentCreate, DepartmentUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: DepartmentCreate, owner_id: int
    ) -> Department:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Department]:
        return (
            db.query(self.model)
            .filter(Department.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_hospital(
        self, db: Session, *, hospital_id: int, skip: int = 0, limit: int = 100
    ) -> List[Department]:
        return (
            db.query(self.model)
            .filter(Department.hospital_id == hospital_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


department = CRUDDepartment(Department)
