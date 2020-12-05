from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

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
    if crud.user.is_superuser(current_user):
        hospitals = crud.hospital.get_multi(db, skip=skip, limit=limit)
    else:
        hospitals = crud.hospital.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return hospitals


@router.post("/", response_model=schemas.Hospital)
def create_hospital(
    *,
    db: Session = Depends(deps.get_db),
    hospital_in: schemas.HospitalCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new Hospital.
    """
    hospital = crud.hospital.create_with_owner(db=db, obj_in=hospital_in, owner_id=current_user.id)
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
