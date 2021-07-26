import pandas as pd
from sqlalchemy.sql.expression import asc, desc
from backend.app.app.models.department import Department
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.submission import Submission
from app.models.survey import Survey
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


## ------ Reporting -------

@router.get("/scores")
def get_scores_by_department(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    return Scores for all departments
    """
    departments = db.query(Department).all()
    module_names = list(set([
        _row.module_name for _row in departments
    ]))
    
    list_of_module_reports = []
    for module_name in module_names:
        
        # first find a departments for the module
        departments = db.query(Department).filter(Department.module_name == module_name).all()
        module_obj = {
            'moduleName': module_name,
            'indicators': []
        }
        for department in departments:
            
            # fetch last submission for the department
            surveys = db.query(Survey).filter(Survey.department_id == department.id).all()
            survey_ids = [_row.id for _row in surveys]
            submission = db.query(Submission).filter(Submission.survey_id.in_(survey_ids)) \
                .order_by(desc(Submission.id)).first()
            if submission is None:
                continue
            
            # get scores
            weigtage_list = []
            for answer in submission.answers:
                for option in answer.get('options', []):
                    if option['text'] == answer['answer']:
                        weigtage_list.append(option.get('weigtage', 0))
            
            # adding score along with name of department in module_obj
            module_obj['indicators'].append({
                'name': department.name,
                'score': sum(weigtage_list)/len(weigtage_list) if len(weigtage_list) > 0 else 0
            })
        list_of_module_reports.append(module_obj)

    return {
        'results': list_of_module_reports
    }


@router.get("/scores_by_submissions")
def get_scores_by_submission(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    return Scores for all departments
    """
    departments = db.query(Department).all()
    module_names = list(set([
        _row.module_name for _row in departments
    ]))
    
    list_of_submissions = []
    for module_name in module_names:
        
        # first find a departments for the module
        departments = db.query(Department).filter(Department.module_name == module_name).all()
        for department in departments:
            
            # fetch last submission for the department
            surveys = db.query(Survey).filter(Survey.department_id == department.id).all()
            survey_ids = [_row.id for _row in surveys]
            submissions = db.query(Submission).filter(Submission.survey_id.in_(survey_ids)) \
                .order_by(asc(Submission.id)).all()
            
            if len(submissions) == 0:
                continue
            
            for index, submission in enumerate(submissions):
                # get scores
                weigtage_list = []
                for answer in submission.answers:
                    for option in answer.get('options', []):
                        if option['text'] == answer['answer']:
                            weigtage_list.append(option.get('weigtage', 0))
            
                # add score for single submission
                list_of_submissions.append({
                    'module_name': module_name,
                    'department_name': department.name,
                    'submission_no': index,
                    'score': sum(weigtage_list)/len(weigtage_list) if len(weigtage_list) > 0 else 0
                })
        

    df = pd.DataFrame(list_of_submissions)
    submission_nos = list(df.submission_no.unique())
    submission_nos.sort()

    submissions_list = {}

    for submission_no in submission_nos:
        sub_df = df.loc[df.submission_no == submission_no]
        submissions_list[submission_no] = []
        
        for module_name in list(sub_df.module_name.unique()):
            sub_df_2 = df.loc[
                df.submission_no == submission_no,
                df.module_name == module_name
            ]
            module_obj = {
                'moduleName': module_name,
                'indicators': []
            }
            
            for _, row in sub_df_2.iterrows():
                module_obj.indicators.append({
                    'name': row['department_name'],
                    'score': row['score']
                })
            submissions_list[submission_no].append(module_obj)  
            
    return {
        'results': submissions_list
    }
