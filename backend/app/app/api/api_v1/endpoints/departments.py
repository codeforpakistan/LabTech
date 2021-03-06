from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.submission import Submission
from app.models.survey import Survey
from app.models.department import Department
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Department])
def read_departments(
    db: Session = Depends(deps.get_db),
    hospital_id: int = 0,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve departments.
    """
    if hospital_id == 0:
        departments = crud.department.get_multi(db, skip=skip, limit=limit)
    else:
        departments = crud.department.get_multi_by_hospital(
            db=db, hospital_id=hospital_id, skip=skip, limit=limit
        )
    try:
        for each_dep in departments:
            surveys = db.query(Survey).filter(Survey.department_id == each_dep.id).all()
            each_dep.have_submission =  False
            for survey in surveys:
                submissions = db.query(Submission).filter(Submission.survey_id == survey.id).all()
                if len(submissions) > 0:
                    each_dep.have_submission =  True
    except:
        print("Could not")

    return departments


@router.post("/", response_model=schemas.Department)
def create_department(
    *,
    db: Session = Depends(deps.get_db),
    department_in: schemas.DepartmentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new department.
    """
    department = crud.department.create_with_owner(db=db, obj_in=department_in, owner_id=current_user.id)
    return department


@router.put("/{id}", response_model=schemas.Department)
def update_department(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    department_in: schemas.DepartmentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an department.
    """
    department = crud.department.get(db=db, id=id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    if not crud.user.is_superuser(current_user) and (department.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    department = crud.department.update(db=db, db_obj=department, obj_in=department_in)
    return department


@router.get("/{id}", response_model=schemas.Department)
def read_department(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get department by ID.
    """
    department = crud.department.get(db=db, id=id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    if not crud.user.is_superuser(current_user) and (department.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return department


@router.delete("/{id}", response_model=schemas.Department)
def delete_department(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an department.
    """
    department = crud.department.get(db=db, id=id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    if not crud.user.is_superuser(current_user) and (department.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    department = crud.department.remove(db=db, id=id)
    return department


@router.get("/module_names/all")
def get_all_module_names(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all module names
    """
    departments = db.query(Department).all()
    _module_names = list(set([
        department.module_name for department in departments if department.module_name  is not None
    ]))
    return {
        'modules': _module_names
    }


@router.post("/questions_length")
def get_all_indicator_names_with_ques_length(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get question length for the given indicator names
    """
    departments = db.query(Department).all()
    results = {}
    for department in departments:
        survey = db.query(Survey).filter(Survey.department_id == department.id).first()
#         if (survey.get("questions", [])):
#             print("***")
#             print(survey.questions)
        results[department.name] = 13

    return results
