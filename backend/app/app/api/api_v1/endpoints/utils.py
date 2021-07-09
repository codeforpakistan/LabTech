import os
import shutil
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, File, UploadFile
from pydantic.networks import EmailStr
from fastapi.responses import FileResponse

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils import send_test_email
import os
router = APIRouter()

@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


@router.post("/uploadimage/")
def create_upload_file(file: UploadFile = File(...)):
    filepath = Path(os.getcwd() + '../../../../images') / file.filename
    save_upload_file(file, filepath)
    return {"filename": file.filename}


@router.get("/image/{image_name}")
def get_image(image_name: str = None):
    return FileResponse(f"${os.getcwd()}../../../../images/{image_name}")
