from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.submission import Submission
from app.schemas.submission import SubmissionCreate, SubmissionUpdate


class CRUDSubmission(CRUDBase[Submission, SubmissionCreate, SubmissionUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: SubmissionCreate, owner_id: int
    ) -> Submission:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Submission]:
        return (
            db.query(self.model)
            .filter(Submission.owner_id == owner_id)
            .order_by(Submission.created_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


submission = CRUDSubmission(Submission)
