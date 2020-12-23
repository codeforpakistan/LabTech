from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Survey])
def read_surveys(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    department_id: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Surveys.
    """
    if department_id == 0:
        surveys = crud.survey.get_multi(db, skip=skip, limit=limit)
    else:
        surveys = crud.survey.get_multi_by_department(
            db=db, department_id=department_id, skip=skip, limit=limit
        )
    return surveys


@router.post("/", response_model=schemas.Survey)
def create_survey(
    *,
    db: Session = Depends(deps.get_db),
    survey_in: schemas.SurveyCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new Survey.
    """
    survey = crud.survey.create_with_owner(db=db, obj_in=survey_in, owner_id=current_user.id)
    return survey


@router.put("/{id}", response_model=schemas.Survey)
def update_survey(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    survey_in: schemas.SurveyUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a Survey.
    """
    survey = crud.survey.get(db=db, id=id)
    if not survey:
        raise HTTPException(status_code=404, detail="Hospital not found")
    if not crud.user.is_superuser(current_user) and (survey.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    survey = crud.survey.update(db=db, db_obj=survey, obj_in=survey_in)
    return survey


@router.get("/{id}", response_model=schemas.Survey)
def read_survey(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get Survey by ID.
    """
    survey = crud.survey.get(db=db, id=id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    if not crud.user.is_superuser(current_user) and (survey.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return survey


@router.delete("/{id}", response_model=schemas.Survey)
def delete_survey(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete Survey.
    """
    survey = crud.survey.get(db=db, id=id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    if not crud.user.is_superuser(current_user) and (survey.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    survey = crud.survey.remove(db=db, id=id)
    return survey
