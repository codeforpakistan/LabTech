from sqlalchemy.sql.expression import desc
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
weightage_to_level_dict = {
    '1': 'LOW',
    '2': 'HIGH',
    '3': 'CRITICAL'
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
        if hospital:
            submission.hospital = hospital.name
        if department:
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
                try:
                    weightage += int(answer.get('weightage', 0))
                except:
                    print('String in weitage, submission id:', submission.id)

            for sub_answer in answer.get('sub_questions', []):
                if 'answer' in sub_answer.keys():
                    questions_list.append({
                        'hospital': hospital.name,
                        'department': department.name,
                        'answer': sub_answer['answer'],
                        'question': answer.get('alias', '') + '-' + sub_answer.get('alias', '') if sub_answer.get('alias', '') != '' else sub_answer.get('question', ''),
                        'weightage': str(answer.get('weightage', 0)),
                        'date': submission.created_date
                    })
                
                if sub_answer.get('answer'):
                    try:
                        weightage += int(sub_answer.get('weightage', 0))
                    except:
                        print('String in weitage, submission id:', submission.id)
        
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
        .apply(lambda x: round(round(x[0]/x[1], 2)*100) if x[1] != 0 else 0, axis=1)
    aggs['answer_false_perc'] = aggs[['answer_false', 'count']] \
        .apply(lambda x: round(round(x[0]/x[1], 2)*100) if x[1] != 0 else 0, axis=1)
    aggs = aggs.sort_values(by=['weightage'], ascending=False)
    aggs = aggs.to_dict(orient='records')
    for question in aggs:
        question['color'] = weightage_to_color_dict.get(question.get('weightage', '1'))
        question['weightage'] = weightage_to_level_dict.get(question.get('weightage', '1'))
    
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
                            'question': answer.get('alias', '') + '-' + 
                            sub_answer.get('alias', '') if sub_answer.get('alias', '') != '' else sub_answer.get('question', ''),
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
        .apply(lambda x: round(round(x[0]/x[1], 2)*100) if x[1] != 0 else 0, axis=1)
    aggs['answer_false_perc'] = aggs[['answer_false', 'count']] \
        .apply(lambda x: round(round(x[0]/x[1], 2)*100) if x[1] != 0 else 0, axis=1)
    aggs = aggs.sort_values(by=['weightage'], ascending=False)
    aggs = aggs.to_dict(orient='records')
    for question in aggs:
        question['color'] = weightage_to_color_dict.get(question.get('weightage', '1'))
        question['weightage'] = weightage_to_level_dict.get(question.get('weightage', '1'))

    return {
        'total_submissions': total_submissions,
        'by_question': aggs
    }, 200


@router.get("/by-labs")
def get_submissions_by_lab(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    apply_filter: int = 0,
    lab_id: int = 0,
    submission_no: int = 0
) -> Any:
    """
    Submissions by Lab
    """

    if crud.user.is_superuser(current_user) and apply_filter == 0:
        submissions = db.query(Submission).all()
    elif crud.user.is_superuser(current_user) and apply_filter == 1:
        submissions = db.query(Submission).filter(Submission.submission_no == submission_no).all()
    elif apply_filter == 0:
        submissions = db.query(Submission).filter(Submission.owner_id == current_user.id).all()
    else:
        submissions = db.query(Submission).filter(
            Submission.owner_id == current_user.id,
            Submission.submission_no == submission_no
        ).all()
    
    submissions_list = []
    for submission in submissions:
        if apply_filter == 1:
            if submission.meta.get('id', 0) != lab_id:
                continue
        
        # calculating scores
        weigtage_list = []
        for answer in submission.answers:
            for option in answer.get('options', []):
                if option['text'] == answer['answer']:
                    try:
                        _w = int(option.get('weigtage', 0))
                    except:
                        _w = 0
                    weigtage_list.append(_w)
        try:
            if len(weigtage_list) > 0:
                _score = sum(weigtage_list)/len(weigtage_list)
            else:
                _score = 0
        except Exception as e:
            print('ERROR', str(e))
            _score = 0

        submissions_list.append({
            'submission_no': submission.submission_no,
            'indicatorId': submission.meta.get('indicatorId', 0),
            '_id': submission.meta.get('id', 0),
            'name': submission.meta.get('hospitalName', ''),
            'module_name': submission.meta.get('moduleName', ''),
            'indicator_name': submission.meta.get('indicatorName', ''),
            'answers': submission.answers,
            'score': _score,
            'submission_id': submission.id,
            'created_date': submission.created_date,
            'comment': submission.comment,
            'images': submission.images,
            'user': current_user.full_name
        })
    
    if len(submissions_list) == 0:
        return {
            'success': False,
            'message': 'no submissions found for the filters'
        }

    submissions_df = pd.DataFrame(submissions_list)
    labnames = list(submissions_df.name.unique())
    submissions_by_lab = []
    for labname in labnames:
        submissions_df_by_labname = submissions_df.loc[
            submissions_df.name == labname
        ]
        submissions_df_by_labname = submissions_df_by_labname.sort_values(by=['submission_no'])
        submission_nos = list(map(int, list(submissions_df_by_labname.submission_no.unique())))
        submission_nos.sort()
        lab_id = int(submissions_df_by_labname._id.iloc[0])
        _departments = db.query(Department).filter(Department.hospital_id == lab_id).all()
        
        for submission_no in submission_nos:
            submissions_df_by_labname_by_no = submissions_df_by_labname.loc[
                submissions_df_by_labname.submission_no == submission_no
            ]
            submissions_df_by_labname_by_no = submissions_df_by_labname_by_no.sort_values(by=['created_date'])
            start_date = submissions_df_by_labname_by_no['created_date'].iloc[0]
            end_date = submissions_df_by_labname_by_no['created_date'].iloc[-1]
            
            # converting df into json
            _submissions = submissions_df_by_labname_by_no.to_dict(orient='records')
            
            # append list of submissions by submission no
            submissions_by_lab.append({
                'user': current_user.full_name,
                'name': labname,
                '_id': int(submissions_df_by_labname_by_no._id.iloc[-1]),
                'submission_no': submission_no,
                'submissions': _submissions,
                'completed': int(len(_departments)) == int(len(submissions_df_by_labname_by_no)),
                'start_date': start_date,
                'end_date': end_date
            })

    return submissions_by_lab


@router.get("/report-by-lab-submission")
def get_report_by_lab_submission(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    apply_filter: int = 0,
    lab_id: int = 0,
    submission_no: int = 0
) -> Any:
    """
    Report by submission and lab
    """

    if crud.user.is_superuser(current_user) and submission_no == 0:
        submissions = db.query(Submission).all()
    elif crud.user.is_superuser(current_user) and submission_no != 0:
        submissions = db.query(Submission).filter(Submission.submission_no == submission_no).all()
    elif submission_no == 0:
        submissions = db.query(Submission).filter(Submission.owner_id == current_user.id).all()
    else:
        submissions = db.query(Submission).filter(
            Submission.owner_id == current_user.id,
            Submission.submission_no == submission_no
        ).all()
    
    submissions_list = []
    for submission in submissions:
        if apply_filter == 1:
            if submission.meta.get('id', 0) != lab_id:
                continue
        
        # calculating scores
        weigtage_list = []
        for answer in submission.answers:

            # skip answer if noScore flag is True
            if answer.get('noScore'):
                continue
            
            for option in answer.get('options', []):
                if option['text'] == answer['answer']:
                    try:
                        _w = int(option.get('weigtage', 0))
                    except:
                        _w = 0
                    weigtage_list.append(_w)
        try:
            if len(weigtage_list) > 0:
                _score = sum(weigtage_list)/len(weigtage_list)
            else:
                _score = 0
        except Exception as e:
            print('ERROR', str(e))
            _score = 0

        submissions_list.append({
            'submission_no': submission.submission_no,
            'indicatorId': submission.meta.get('indicatorId', 0),
            '_id': submission.meta.get('id', 0),
            'name': submission.meta.get('hospitalName', ''),
            'module_name': submission.meta.get('moduleName', '').strip(),
            'indicator_name': submission.meta.get('indicatorName', ''),
            'answers': submission.answers,
            'score': _score,
            'submission_id': submission.id,
            'created_date': submission.created_date,
            'comment': submission.comment,
            'images': submission.images,
            'user': current_user.full_name
        })
    
    # incase of single submission request
    # return complete details including answers
    # if submission_no > 0:
    #     return submissions_list

    if len(submissions_list) == 0:
        return {
            'success': False,
            'message': 'no submissions found for the filters'
        }

    df = pd.DataFrame(submissions_list)
    aggs = df[[
        'module_name', 'indicator_name', 'score', 'answers'
    ]].groupby(['module_name', 'indicator_name', 'answers'], as_index=False).mean()
    
    report_list = {}
    for module_name in list(aggs.module_name.unique()):
        aggs_by_module = aggs.loc[
            aggs.module_name == module_name
        ]
        report_list[module_name] = {
            'indicators': aggs_by_module.to_dict(orient='records'),
            'score': sum(aggs_by_module.score)/len(aggs_by_module)
        }
    
    # report_dict = aggs.to_dict(orient='records')

    return report_list


@router.get("/submission_nos/by-lab")
def get_submission_nos_by_lab(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    lab_id: int = 0,
) -> Any:
    """
    Submissions by Lab
    """
    departments = db.query(Department).filter(Department.hospital_id == lab_id).all()
    _department_ids = [department.id for department in departments]
    _survey_ids = [
        survey.id for survey in db.query(Survey).filter(Survey.department_id.in_(_department_ids)).all()
    ]
    submission_nos = [
        submission.submission_no for submission in db.query(Submission).filter(Submission.survey_id.in_(_survey_ids)).all()
    ]
    submission_nos = list(set(submission_nos))
    submission_nos.sort()
    return {'lab_id': lab_id, 'submission_nos': submission_nos}


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

    if submission_in.submission_no == 0:
        # finding submission no
        survey = db.query(Survey).filter(Survey.id == submission_in.survey_id).first()
        if survey is None:
            submission_in.submission_no = 1
        else:
            # find via departments
            surveys = db.query(Survey).filter(Survey.department_id == survey.department_id).all()
            survey_ids = [_doc.id for _doc in surveys]
            submission = db.query(Submission).filter(Submission.survey_id.in_(survey_ids)) \
                .order_by(desc(Submission.submission_no)).first()
            
            submission_in.submission_no = 1
            if submission is not None and submission.submission_no is not None:
                submission_in.submission_no = submission.submission_no  + 1

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
