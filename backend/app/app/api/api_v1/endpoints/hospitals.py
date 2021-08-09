from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from app.models.survey import Survey
from app.models.department import Department
from app.models.hospital import Hospital
from app.models.submission import Submission

router = APIRouter()


@router.get("/", response_model=List[schemas.Hospital])
def read_hospitals(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Hospitals.
    """
    # Return all if logged in user is super user
    if current_user.is_superuser:
        return crud.hospital.get_multi(db, skip=skip, limit=limit)
    
    # Return only those hospitals which are allowed to the logged in user
    allowed_hospitals_ids = [
        hospital['id'] for hospital in current_user.allowed_hospitals
    ]
    hospitals = crud.hospital.get_multi(db, skip=skip, limit=limit)
    allowed_hospitals = [
        hospital for hospital in hospitals if hospital.id in allowed_hospitals_ids
    ]
    return allowed_hospitals


@router.post("/", response_model=schemas.Hospital)
def create_hospital(
    *,
    db: Session = Depends(deps.get_db),
    hospital_in: schemas.HospitalCreate,
    create_indicators: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new Hospital.
    """

    hospital = crud.hospital.create_with_owner(
        db=db, obj_in=hospital_in, owner_id=current_user.id
    )
    
    if create_indicators and current_user.is_superuser:
        # find the example lab/hospital for the prefil data
        example_hospital = db.query(Hospital).filter(Hospital.name == "Islamabad Diagnostic Centre").first()
        example_departments = db.query(Department).filter(Department.hospital_id == example_hospital.id)
        for department in example_departments:
            d_in = schemas.DepartmentCreate(name=department.name,hospital_id=hospital.id)
            d_in.hospital_id = hospital.id
            d_in.name = department.name
            d_in.module_name = department.module_name
            new_depart = crud.department.create_with_owner(db=db, obj_in=d_in, owner_id=current_user.id)

            example_surveys = db.query(Survey).filter(Survey.department_id == department.id)
            for survey in example_surveys:
                s_in = schemas.SurveyCreate()
                s_in.department_id = new_depart.id
                s_in.name = survey.name
                s_in.questions = survey.questions
                new_survey = crud.survey.create_with_owner(db=db, obj_in=s_in, owner_id=current_user.id)
    
    return hospital


@router.put("/{id}", response_model=schemas.Hospital)
def update_hospital(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    hospital_in: schemas.HospitalUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a Hospital.
    """
    hospital = crud.hospital.get(db=db, id=id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    if not crud.user.is_superuser(current_user) and (hospital.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    hospital = crud.hospital.update(db=db, db_obj=hospital, obj_in=hospital_in)
    return hospital


@router.get("/{id}", response_model=schemas.Hospital)
def read_hospital(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get Hospital by ID.
    """
    hospital = crud.hospital.get(db=db, id=id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    if not crud.user.is_superuser(current_user) and (hospital.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return hospital


@router.delete("/{id}", response_model=schemas.Hospital)
def delete_hospital(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete Hospital.
    """
    hospital = crud.hospital.get(db=db, id=id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    if not crud.user.is_superuser(current_user) and (hospital.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    hospital = crud.hospital.remove(db=db, id=id)
    return hospital
