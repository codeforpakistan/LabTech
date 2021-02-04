import pandas as pd
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

weightage_to_color_dict = {
    '1': '#02951B',
    '2': '#FE8300',
    '3': '#FE0000'
}

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

    for submission in list(submissions):
        survey = db.query(Survey).filter(Survey.id == submission.survey_id).first()
        department = db.query(Department).filter(Department.id == survey.department_id).first()
        hospital = db.query(Hospital).filter(Hospital.id == department.hospital_id).first()
        submission.hospital = hospital.name
        submission.department = department.name
    return submissions


@router.get("/report/by-questions")
def read_submissions_report(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Geneate report for submition
    """
    submissions = crud.submission.get_multi(db)
    total_submissions = len(submissions)
    submissions_list = []
    questions_list = []
    for submission in list(submissions):
        survey = db.query(Survey).filter(Survey.id == submission.survey_id).first()
        department = db.query(Department).filter(Department.id == survey.department_id).first()
        hospital = db.query(Hospital).filter(Hospital.id == department.hospital_id).first()
        submission.hospital = hospital.name
        submission.department = department.name
        weightage = 0
        
        
        for answer in submission.answers:
            if 'answer' in answer.keys():
                questions_list.append({
                    'hospital': hospital.name,
                    'department': department.name,
                    'answer': answer['answer'],
                    'question': answer.get('alias', '') if answer.get('alias', '') != '' else answer.get('question', ''),
                    'weightage': str(answer.get('weightage', 0)),
                    'date': submission.created_date
                })

            if answer.get('answer'):
                weightage += answer.get('weightage', 0)

            for sub_answer in answer.get('sub_questions', []):
                if 'answer' in sub_answer.keys():
                    questions_list.append({
                        'hospital': hospital.name,
                        'department': department.name,
                        'answer': sub_answer['answer'],
                        'question': sub_answer.get('alias', '') if sub_answer.get('alias', '') != '' else sub_answer.get('question', ''),
                        'weightage': str(answer.get('weightage', 0)),
                        'date': submission.created_date
                    })

                if sub_answer.get('answer'):
                    weightage += sub_answer.get('weightage', 0)
        submissions_list.append({
            'hospital': hospital.name,
            'department': department.name,
            'weightage': weightage,
            'date': submission.created_date
        })

    df = pd.DataFrame(questions_list)
    if len(df) < 1:
        # no submissions found, so no aggs needed.
        return {
            'total_submissions': 0,
            'by_question': [],
            'message': 'No submissions found to aggregate on.'
        }, 200
    df['count'] = 1
    df['answer_true'] = df['answer'].apply(lambda x: 1 if x == True else 0)
    df['answer_false'] = df['answer'].apply(lambda x: 0 if x == True else 1)
    aggs = df[['question', 'weightage', 'answer_true', 'answer_false', 'count']] \
        .groupby(['question', 'weightage'], as_index=False).sum()
    aggs['answer_true_perc'] = aggs[['answer_true', 'count']] \
        .apply(lambda x: round(x[0]/x[1], 2)*100 if x[1] != 0 else 0, axis=1)
    aggs['answer_false_perc'] = aggs[['answer_false', 'count']] \
        .apply(lambda x: round(x[0]/x[1], 2)*100 if x[1] != 0 else 0, axis=1)
    aggs = aggs.to_dict(orient='records')
    for question in aggs:
        question['color'] = weightage_to_color_dict.get(question.get('weightage', '1'))

    return {
        'total_submissions': total_submissions,
        'by_question': aggs
    }, 200


@router.get("/report/by-questions/{hospital_id}/{department_id}")
def read_submissions_report_by_hospital(
    db: Session = Depends(deps.get_db),
    hospital_id: int = 0,
    department_id: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Geneate report for submition by hospital
    """
    total_submissions = 0
    questions_list = []
    hospital = hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    for department in hospital.departments:
        if department.id != department_id and department_id != 0:
            continue
        survey = db.query(Survey).filter(Survey.department_id == department.id).first()
        submissions = db.query(Submission).filter(Submission.survey_id == survey.id).all()
        total_submissions += len(submissions)
        for submission in submissions:
            for answer in submission.answers:
                if 'answer' in answer.keys():
                    questions_list.append({
                        'hospital': hospital.name,
                        'department': department.name,
                        'answer': answer['answer'],
                        'question': answer.get('alias', '') if answer.get('alias', '') != '' else answer.get('question', ''),
                        'weightage': str(answer.get('weightage', 0)),
                        'date': submission.created_date
                    })

                for sub_answer in answer.get('sub_questions', []):
                    if 'answer' in sub_answer.keys():
                        questions_list.append({
                            'hospital': hospital.name,
                            'department': department.name,
                            'answer': sub_answer['answer'],
                            'question': sub_answer.get('alias', '') if sub_answer.get('alias', '') != '' else sub_answer.get('question', ''),
                            'weightage': str(answer.get('weightage', 0)),
                            'date': submission.created_date
                        })


    df = pd.DataFrame(questions_list)
    if len(df) < 1:
        # no submissions found, so no aggs needed.
        return {
            'total_submissions': 0,
            'by_question': [],
            'message': 'No submissions found to aggregate on.'
        }, 200

    df['count'] = 1
    df['answer_true'] = df['answer'].apply(lambda x: 1 if x == True else 0)
    df['answer_false'] = df['answer'].apply(lambda x: 0 if x == True else 1)
    aggs = df[['question', 'weightage', 'answer_true', 'answer_false', 'count']] \
        .groupby(['question', 'weightage'], as_index=False).sum()
    aggs['answer_true_perc'] = aggs[['answer_true', 'count']] \
        .apply(lambda x: round(x[0]/x[1],2)*100 if x[1] != 0 else 0, axis=1)
    aggs['answer_false_perc'] = aggs[['answer_false', 'count']] \
        .apply(lambda x: round(x[0]/x[1],2)*100 if x[1] != 0 else 0, axis=1)
    aggs = aggs.to_dict(orient='records')
    for question in aggs:
        question['color'] = weightage_to_color_dict.get(question.get('weightage', '1'))

    return {
        'total_submissions': total_submissions,
        'by_question': aggs
    }, 200


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
    print(submission_in.answers)
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
