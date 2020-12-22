from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from app.models.survey import Survey
from app.models.department import Department
from app.models.hospital import Hospital


router = APIRouter()


@router.get("/", response_model=List[schemas.Submission])
def read_submissions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve submissions.
    """
    if False:# crud.user.is_superuser(current_user):
        submissions = crud.submission.get_multi(db, skip=skip, limit=limit)
    else:
        submissions = crud.submission.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )

    # get survey with survey id
    # get department by department id
    # get hospital by hospital id
    # for submission in submissions:
    #     survey = survey.get(db=db, id=submission.survey_id)
    #     department = department.get(db=db, id=survey.department_id)
    #     hospital = hospital.get(db=db, id=department.hospital_id)
    #     submission['hospital'] = hospital.name


    print('Submissions', submissions)
    for submission in list(submissions):
        survey = db.query(Survey).filter(Survey.id == submission.survey_id).first()
        department = db.query(Department).filter(Department.id == survey.department_id).first()
        hospital = db.query(Hospital).filter(Hospital.id == department.hospital_id).first()
        submission.hospital = hospital.name
        submission.department = department.name
    return submissions


@router.post("/", response_model=schemas.Submission)
def create_submission(
    *,
    db: Session = Depends(deps.get_db),
    submission_in: schemas.SubmissionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new submission.
    """
    submission = crud.submission.create_with_owner(db=db, obj_in=submission_in, owner_id=current_user.id)
    
    return submission


@router.put("/{id}", response_model=schemas.Submission)
def update_submission(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    submission_in: schemas.SubmissionUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update existing submission.
    """
    submission = crud.submission.get(db=db, id=id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    if not crud.user.is_superuser(current_user) and (submission.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    submission = crud.submission.update(db=db, db_obj=submission, obj_in=submission_in)
    return submission


@router.get("/{id}", response_model=schemas.Submission)
def read_submission(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get submission by ID.
    """
    submission = crud.submission.get(db=db, id=id)
    if not submission:
        raise HTTPException(status_code=404, detail="submission not found")
    if not crud.user.is_superuser(current_user) and (submission.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return submission


@router.delete("/{id}", response_model=schemas.Submission)
def delete_submission(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete submission.
    """
    submission = crud.submission.get(db=db, id=id)
    if not submission:
        raise HTTPException(status_code=404, detail="submission not found")
    if not crud.user.is_superuser(current_user) and (submission.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    submission = crud.submission.remove(db=db, id=id)
    return submission
