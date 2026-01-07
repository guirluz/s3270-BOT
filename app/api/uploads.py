from fastapi import APIRouter, UploadFile, File
import os
import uuid

from app.utils.responses import build_response
from app.db.session import SessionLocal
from app.db.models.upload import Upload
from app.tasks.upload_tasks import process_upload_task

router = APIRouter(prefix="/uploads", tags=["Uploads"])


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("")
def upload_file(file: UploadFile = File(...)):
    """
    Sube un archivo y lanza su procesamiento asíncrono.
    """

    db = SessionLocal()

    try:
        # ------------------------------
        # Validaciones básicas
        # ------------------------------
        if not file.filename:
            return build_response(400, "File name is required", None)

        ext = os.path.splitext(file.filename)[1].lower()

        if ext not in (".csv", ".xlsx"):
            return build_response(
                400,
                "Only CSV or XLSX files are allowed",
                None
            )

        # ------------------------------
        # Guardar archivo en disco
        # ------------------------------
        file_id = uuid.uuid4().hex
        filename = f"{file_id}{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # ------------------------------
        # Registrar upload en DB
        # ------------------------------
        upload = Upload(
            filename=file.filename,
            file_path=file_path,
        )

        db.add(upload)
        db.commit()
        db.refresh(upload)

        # ------------------------------
        # Lanzar tarea Celery
        # ------------------------------
        task = process_upload_task.delay(upload.id)

        return build_response(
            http_code=202,
            message="Upload accepted and processing started",
            data={
                "upload_id": upload.id,
                "task_id": task.id,
                "state": task.state
            }
        )

    except Exception as exc:
        return build_response(
            500,
            "Upload failed",
            str(exc)
        )

    finally:
        db.close()

