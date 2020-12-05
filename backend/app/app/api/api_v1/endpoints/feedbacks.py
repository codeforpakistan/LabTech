from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Feedback])
def read_feedbacks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve feedbacks.
    """
    if crud.user.is_superuser(current_user):
        feedbacks = crud.feedback.get_multi(db, skip=skip, limit=limit)
    else:
        feedbacks = crud.feedback.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return feedbacks


@router.post("/", response_model=schemas.Feedback)
def create_feedback(
    *,
    db: Session = Depends(deps.get_db),
    feedback_in: schemas.FeedbackCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new feedback.
    """
    feedback = crud.feedback.create_with_owner(db=db, obj_in=feedback_in, owner_id=current_user.id)
    return feedback


@router.put("/{id}", response_model=schemas.Feedback)
def update_feedback(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    feedback_in: schemas.FeedbackUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an Feedback.
    """
    feedback = crud.feedback.get(db=db, id=id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    if not crud.user.is_superuser(current_user) and (feedback.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    feedback = crud.feedback.update(db=db, db_obj=feedback, obj_in=feedback_in)
    return feedback


@router.get("/{id}", response_model=schemas.Feedback)
def read_feedback(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get feedback by ID.
    """
    feedback = crud.feedback.get(db=db, id=id)
    if not feedback:
        raise HTTPException(status_code=404, detail="feedback not found")
    if not crud.user.is_superuser(current_user) and (feedback.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return feedback


@router.delete("/{id}", response_model=schemas.Feedback)
def delete_feedback(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an feedback.
    """
    feedback = crud.feedback.get(db=db, id=id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    if not crud.user.is_superuser(current_user) and (feedback.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    feedback = crud.feedback.remove(db=db, id=id)
    return feedback
